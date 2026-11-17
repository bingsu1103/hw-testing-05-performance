#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
sut_dir="${repo_dir}/sut/eshop-sut"

if [[ ! -d "${sut_dir}/.git" ]]; then
  mkdir -p "${repo_dir}/sut"
  git clone https://github.com/ttbhanh/eshop-sut.git "$sut_dir"
fi

npm ci --prefix "${sut_dir}/backend"
echo "SUT prepared at ${sut_dir}. Start it with: npm start --prefix '${sut_dir}/backend'"

