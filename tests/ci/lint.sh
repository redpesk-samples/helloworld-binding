command -v clang-format 2>/dev/null 2>&1 || sudo dnf install -y clang-tools-extra

rm -f clang-format
wget http://git.ovh.iot/iotbzh/iot-devtools/-/raw/master/clang-format
git ls-files \
  | grep -E '\.(c|cc|cpp|cxx|h|hh|hpp|hxx)$' \
  | xargs clang-format --dry-run --style=file:clang-format --Werror || exit 1
