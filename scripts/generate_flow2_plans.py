#!/usr/bin/env python3
"""Generate the four HW05 JMeter plans from the binding Flow 2 workflow."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
CSV_VARIABLES = (
    "name_prefix,password,search,product_id,product_name,product_price,quantity,"
    "total_amount,coupon_code,expected_final_amount,shipping_address"
)


@dataclass(frozen=True)
class Scenario:
    name: str
    threads: int
    ramp_seconds: int
    loops: int
    scheduler: bool
    duration_seconds: int
    listener_class: str
    listener_gui: str
    listener_name: str


SCENARIOS = (
    Scenario("Load", 20, 60, 5, False, 0, "ResultCollector", "ViewResultsFullVisualizer", "Load View - View Results Tree"),
    Scenario("Stress", 80, 120, 10, False, 0, "ResultCollector", "SummaryReport", "Stress View - Summary Report"),
    Scenario("Spike", 150, 5, 3, False, 0, "ResultCollector", "StatVisualizer", "Spike View - Aggregate Report"),
    Scenario("Soak", 25, 60, -1, True, 720, "ResultCollector", "SummaryReport", "Soak View - Summary Report"),
)


def raw_body(value: str) -> str:
    return dedent(
        f"""
        <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
        <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
          <collectionProp name="Arguments.arguments">
            <elementProp name="" elementType="HTTPArgument">
              <boolProp name="HTTPArgument.always_encode">false</boolProp>
              <stringProp name="Argument.value">{value}</stringProp>
              <stringProp name="Argument.metadata">=</stringProp>
            </elementProp>
          </collectionProp>
        </elementProp>
        """
    ).strip()


def http_sampler(name: str, path: str, method: str, body: str | None = None) -> str:
    arguments = raw_body(body) if body is not None else (
        '<elementProp name="HTTPsampler.Arguments" elementType="Arguments">'
        '<collectionProp name="Arguments.arguments"/></elementProp>'
    )
    return dedent(
        f"""
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="{name}" enabled="true">
          {arguments}
          <stringProp name="HTTPSampler.path">{path}</stringProp>
          <stringProp name="HTTPSampler.method">{method}</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
        </HTTPSamplerProxy>
        """
    ).strip()


def response_assertion(name: str, code: int = 200) -> str:
    return dedent(
        f"""
        <ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="{name}" enabled="true">
          <collectionProp name="Asserion.test_strings"><stringProp name="{code}">{code}</stringProp></collectionProp>
          <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
          <boolProp name="Assertion.assume_success">false</boolProp>
          <intProp name="Assertion.test_type">8</intProp>
        </ResponseAssertion><hashTree/>
        """
    ).strip()


def json_extractor(name: str, references: str, expressions: str, defaults: str) -> str:
    return dedent(
        f"""
        <JSONPostProcessor guiclass="JSONPostProcessorGui" testclass="JSONPostProcessor" testname="{name}" enabled="true">
          <stringProp name="JSONPostProcessor.referenceNames">{references}</stringProp>
          <stringProp name="JSONPostProcessor.jsonPathExprs">{expressions}</stringProp>
          <stringProp name="JSONPostProcessor.match_numbers">1</stringProp>
          <stringProp name="JSONPostProcessor.defaultValues">{defaults}</stringProp>
        </JSONPostProcessor><hashTree/>
        """
    ).strip()


def bearer_header() -> str:
    return dedent(
        """
        <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="Bearer Token" enabled="true">
          <collectionProp name="HeaderManager.headers">
            <elementProp name="" elementType="Header">
              <stringProp name="Header.name">Authorization</stringProp>
              <stringProp name="Header.value">Bearer ${auth_token}</stringProp>
            </elementProp>
          </collectionProp>
        </HeaderManager><hashTree/>
        """
    ).strip()


def render_workflow() -> str:
    register = http_sampler(
        "01 Auth - Register",
        "/api/register",
        "POST",
        "{&quot;name&quot;:&quot;${flow_name}&quot;,&quot;email&quot;:&quot;${flow_email}&quot;,&quot;password&quot;:&quot;${password}&quot;}",
    )
    login = http_sampler(
        "02 Auth - Login",
        "/api/login",
        "POST",
        "{&quot;email&quot;:&quot;${flow_email}&quot;,&quot;password&quot;:&quot;${password}&quot;}",
    )
    search = dedent(
        """
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="03 Read - Search Products" enabled="true">
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
            <collectionProp name="Arguments.arguments">
              <elementProp name="search" elementType="HTTPArgument">
                <boolProp name="HTTPArgument.always_encode">true</boolProp>
                <stringProp name="Argument.name">search</stringProp>
                <stringProp name="Argument.value">${search}</stringProp>
                <stringProp name="Argument.metadata">=</stringProp>
                <boolProp name="HTTPArgument.use_equals">true</boolProp>
              </elementProp>
            </collectionProp>
          </elementProp>
          <stringProp name="HTTPSampler.path">/api/products</stringProp>
          <stringProp name="HTTPSampler.method">GET</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
        </HTTPSamplerProxy>
        """
    ).strip()
    detail = http_sampler("04 Read - Product Detail", "/api/products/${product_id}", "GET")
    cart = http_sampler(
        "05 Transaction - Add to Cart",
        "/api/cart",
        "POST",
        "{&quot;id&quot;:${product_id},&quot;name&quot;:&quot;${product_name}&quot;,&quot;price&quot;:${product_price},&quot;quantity&quot;:${quantity}}",
    )
    coupon = http_sampler(
        "06 Transaction - Apply Coupon",
        "/api/apply-coupon",
        "POST",
        "{&quot;code&quot;:&quot;${coupon_code}&quot;,&quot;total_amount&quot;:${total_amount},&quot;user_id&quot;:${user_id}}",
    )
    checkout = http_sampler(
        "07 Transaction - Checkout",
        "/api/checkout",
        "POST",
        "{&quot;items&quot;:[{&quot;id&quot;:${product_id},&quot;quantity&quot;:${quantity}}],&quot;total_amount&quot;:${final_amount},&quot;coupon_id&quot;:${coupon_id},&quot;shipping_address&quot;:&quot;${shipping_address}&quot;}",
    )
    usage = http_sampler(
        "08 Transaction - Record Coupon Usage",
        "/api/coupon-usage",
        "POST",
        "{&quot;coupon_id&quot;:${coupon_id}}",
    )
    register_script = (
        "def runId = props.get('flow2_run_id'); "
        "if (runId == null) { synchronized(props) { runId = props.get('flow2_run_id'); "
        "if (runId == null) { runId = Long.toString(System.currentTimeMillis()); props.put('flow2_run_id', runId) } } }; "
        "def suffix = ctx.getThreadNum() + '_' + vars.getIteration(); "
        "vars.put('flow_email', 'flow2_' + runId + '_' + suffix + '@example.test'); "
        "vars.put('flow_name', vars.get('name_prefix') + ' ' + suffix)"
    )
    return "\n".join(
        [
            register,
            "<hashTree>",
            f'<JSR223PreProcessor guiclass="TestBeanGUI" testclass="JSR223PreProcessor" testname="Create unique Flow 2 identity" enabled="true"><stringProp name="scriptLanguage">groovy</stringProp><stringProp name="parameters"></stringProp><stringProp name="filename"></stringProp><stringProp name="cacheKey">true</stringProp><stringProp name="script">{register_script}</stringProp></JSR223PreProcessor><hashTree/>',
            response_assertion("Register returns HTTP 200"),
            json_extractor("Extract Registered User ID", "user_id", "$.id", "NOT_FOUND"),
            '<JSR223Assertion guiclass="TestBeanGUI" testclass="JSR223Assertion" testname="Registered user ID must be present" enabled="true"><stringProp name="scriptLanguage">groovy</stringProp><stringProp name="parameters"></stringProp><stringProp name="filename"></stringProp><stringProp name="cacheKey">true</stringProp><stringProp name="script">if (vars.get(\'user_id\') == \'NOT_FOUND\') { AssertionResult.setFailure(true); AssertionResult.setFailureMessage(\'Missing registered user ID\') }</stringProp></JSR223Assertion><hashTree/>',
            "</hashTree>",
            login,
            "<hashTree>",
            response_assertion("Login returns HTTP 200"),
            json_extractor("Extract JWT", "auth_token", "$.token", "NOT_FOUND"),
            '<JSR223Assertion guiclass="TestBeanGUI" testclass="JSR223Assertion" testname="JWT must be present" enabled="true"><stringProp name="scriptLanguage">groovy</stringProp><stringProp name="parameters"></stringProp><stringProp name="filename"></stringProp><stringProp name="cacheKey">true</stringProp><stringProp name="script">if (vars.get(\'auth_token\') == \'NOT_FOUND\') { AssertionResult.setFailure(true); AssertionResult.setFailureMessage(\'Missing JWT token\') }</stringProp></JSR223Assertion><hashTree/>',
            "</hashTree>",
            search,
            f"<hashTree>{response_assertion('Product search returns HTTP 200')}</hashTree>",
            detail,
            f"<hashTree>{response_assertion('Product detail returns HTTP 200')}</hashTree>",
            cart,
            f"<hashTree>{bearer_header()}{response_assertion('Cart returns HTTP 200')}</hashTree>",
            coupon,
            "<hashTree>",
            response_assertion("Apply coupon returns HTTP 200"),
            json_extractor("Extract Coupon Result", "coupon_id;final_amount", "$.coupon_id;$.final_amount", "NOT_FOUND;NOT_FOUND"),
            '<JSR223Assertion guiclass="TestBeanGUI" testclass="JSR223Assertion" testname="Coupon final amount must match CSV" enabled="true"><stringProp name="scriptLanguage">groovy</stringProp><stringProp name="parameters"></stringProp><stringProp name="filename"></stringProp><stringProp name="cacheKey">true</stringProp><stringProp name="script">if (vars.get(\'final_amount\') != vars.get(\'expected_final_amount\')) { AssertionResult.setFailure(true); AssertionResult.setFailureMessage(\'Expected final_amount=\' + vars.get(\'expected_final_amount\') + \', got \'+ vars.get(\'final_amount\')) }</stringProp></JSR223Assertion><hashTree/>',
            "</hashTree>",
            checkout,
            "<hashTree>",
            bearer_header(),
            response_assertion("Checkout returns HTTP 200"),
            json_extractor("Extract Order ID", "order_id", "$.orderId", "NOT_FOUND"),
            '<JSR223Assertion guiclass="TestBeanGUI" testclass="JSR223Assertion" testname="Order ID must be present" enabled="true"><stringProp name="scriptLanguage">groovy</stringProp><stringProp name="parameters"></stringProp><stringProp name="filename"></stringProp><stringProp name="cacheKey">true</stringProp><stringProp name="script">if (vars.get(\'order_id\') == \'NOT_FOUND\') { AssertionResult.setFailure(true); AssertionResult.setFailureMessage(\'Missing order ID\') }</stringProp></JSR223Assertion><hashTree/>',
            "</hashTree>",
            usage,
            f"<hashTree>{bearer_header()}{response_assertion('Coupon usage returns HTTP 200')}</hashTree>",
        ]
    )


def render_plan(scenario: Scenario) -> str:
    if scenario.scheduler:
        loop_value = "-1"
        group_label = f"{scenario.name} - ${{__P(threads,{scenario.threads})}} users, ${{__P(ramp_seconds,{scenario.ramp_seconds})}}s ramp, ${{__P(duration_seconds,{scenario.duration_seconds})}}s duration"
        duration = f'${{__P(duration_seconds,{scenario.duration_seconds})}}'
    else:
        loop_value = f'${{__P(loops,{scenario.loops})}}'
        group_label = f"{scenario.name} - ${{__P(threads,{scenario.threads})}} users, ${{__P(ramp_seconds,{scenario.ramp_seconds})}}s ramp, ${{__P(loops,{scenario.loops})}} iterations"
        duration = ""

    return dedent(
        f"""\
        <?xml version="1.0" encoding="UTF-8"?>
        <jmeterTestPlan version="1.2" properties="5.0" jmeter="5.6.3">
          <hashTree>
            <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="23120205 {scenario.name} - Flow 2 Search and Coupon" enabled="true">
              <stringProp name="TestPlan.comments">CSV-driven register -&gt; login -&gt; product search/detail -&gt; cart -&gt; coupon -&gt; checkout workflow.</stringProp>
              <boolProp name="TestPlan.functional_mode">false</boolProp>
              <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
              <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
                <collectionProp name="Arguments.arguments">
                  <elementProp name="host" elementType="Argument"><stringProp name="Argument.name">host</stringProp><stringProp name="Argument.value">${{__P(host,localhost)}}</stringProp><stringProp name="Argument.metadata">=</stringProp></elementProp>
                  <elementProp name="port" elementType="Argument"><stringProp name="Argument.name">port</stringProp><stringProp name="Argument.value">${{__P(port,3000)}}</stringProp><stringProp name="Argument.metadata">=</stringProp></elementProp>
                  <elementProp name="protocol" elementType="Argument"><stringProp name="Argument.name">protocol</stringProp><stringProp name="Argument.value">${{__P(protocol,http)}}</stringProp><stringProp name="Argument.metadata">=</stringProp></elementProp>
                </collectionProp>
              </elementProp>
              <stringProp name="TestPlan.user_define_classpath"></stringProp>
            </TestPlan>
            <hashTree>
              <ConfigTestElement guiclass="HttpDefaultsGui" testclass="ConfigTestElement" testname="HTTP Request Defaults" enabled="true">
                <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true"><collectionProp name="Arguments.arguments"/></elementProp>
                <stringProp name="HTTPSampler.domain">${{host}}</stringProp><stringProp name="HTTPSampler.port">${{port}}</stringProp><stringProp name="HTTPSampler.protocol">${{protocol}}</stringProp>
                <stringProp name="HTTPSampler.connect_timeout">5000</stringProp><stringProp name="HTTPSampler.response_timeout">10000</stringProp><stringProp name="HTTPSampler.contentEncoding">UTF-8</stringProp><stringProp name="HTTPSampler.implementation">HttpClient4</stringProp>
              </ConfigTestElement><hashTree/>
              <HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="Default JSON Headers" enabled="true"><collectionProp name="HeaderManager.headers"><elementProp name="" elementType="Header"><stringProp name="Header.name">Content-Type</stringProp><stringProp name="Header.value">application/json</stringProp></elementProp><elementProp name="" elementType="Header"><stringProp name="Header.name">Accept</stringProp><stringProp name="Header.value">application/json</stringProp></elementProp></collectionProp></HeaderManager><hashTree/>
              <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="{group_label}" enabled="true">
                <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
                <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="Loop Controller" enabled="true"><boolProp name="LoopController.continue_forever">false</boolProp><stringProp name="LoopController.loops">{loop_value}</stringProp></elementProp>
                <stringProp name="ThreadGroup.num_threads">${{__P(threads,{scenario.threads})}}</stringProp><stringProp name="ThreadGroup.ramp_time">${{__P(ramp_seconds,{scenario.ramp_seconds})}}</stringProp><boolProp name="ThreadGroup.same_user_on_next_iteration">false</boolProp><boolProp name="ThreadGroup.scheduler">{str(scenario.scheduler).lower()}</boolProp><stringProp name="ThreadGroup.duration">{duration}</stringProp><stringProp name="ThreadGroup.delay"></stringProp>
              </ThreadGroup>
              <hashTree>
                <CSVDataSet guiclass="TestBeanGUI" testclass="CSVDataSet" testname="CSV Flow 2 Data" enabled="true"><stringProp name="filename">${{__P(csv_file,data/users.csv)}}</stringProp><stringProp name="fileEncoding">UTF-8</stringProp><stringProp name="variableNames">{CSV_VARIABLES}</stringProp><boolProp name="ignoreFirstLine">true</boolProp><stringProp name="delimiter">,</stringProp><boolProp name="quotedData">true</boolProp><boolProp name="recycle">true</boolProp><boolProp name="stopThread">false</boolProp><stringProp name="shareMode">shareMode.all</stringProp></CSVDataSet><hashTree/>
                <UniformRandomTimer guiclass="UniformRandomTimerGui" testclass="UniformRandomTimer" testname="Human think time 0.5-2.0s" enabled="true"><stringProp name="ConstantTimer.delay">500</stringProp><stringProp name="RandomTimer.range">1500</stringProp></UniformRandomTimer><hashTree/>
                {render_workflow()}
                <ResultCollector guiclass="{scenario.listener_gui}" testclass="{scenario.listener_class}" testname="{scenario.listener_name}" enabled="true"><boolProp name="ResultCollector.error_logging">false</boolProp><objProp><name>saveConfig</name><value class="SampleSaveConfiguration"><time>true</time><latency>true</latency><timestamp>true</timestamp><success>true</success><label>true</label><code>true</code><message>true</message><threadName>true</threadName><dataType>true</dataType><encoding>false</encoding><assertions>true</assertions><subresults>true</subresults><responseData>false</responseData><samplerData>false</samplerData><xml>false</xml><fieldNames>true</fieldNames><responseHeaders>false</responseHeaders><requestHeaders>false</requestHeaders><responseDataOnError>false</responseDataOnError><saveAssertionResultsFailureMessage>true</saveAssertionResultsFailureMessage><assertionsResultsToSave>0</assertionsResultsToSave><bytes>true</bytes><sentBytes>true</sentBytes><url>true</url><threadCounts>true</threadCounts><idleTime>true</idleTime><connectTime>true</connectTime></value></objProp><stringProp name="filename"></stringProp></ResultCollector><hashTree/>
              </hashTree>
            </hashTree>
          </hashTree>
        </jmeterTestPlan>
        """
    ).lstrip()


def main() -> int:
    output_dir = ROOT / "test-plans"
    for scenario in SCENARIOS:
        path = output_dir / f"23120205_{scenario.name}_20261117.jmx"
        path.write_text(render_plan(scenario), encoding="utf-8")
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
