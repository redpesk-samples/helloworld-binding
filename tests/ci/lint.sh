command -v clang-format 2>/dev/null 2>&1 || sudo dnf install -y clang-tools-extra

rm -f clang-format
wget https://download.redpesk.bzh/redpesk-ci/redpesk-format-style/clang-format
git ls-files \
  | grep -E '\.(c|cc|cpp|cxx|h|hh|hpp|hxx)$' \
  | xargs clang-format --dry-run --style=file:clang-format --Werror || exit 1
