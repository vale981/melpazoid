"""Entrypoint to melpazoid."""
import operator
import shutil
from typing import Iterator, List, TextIO, Tuple
_RETURN_CODE = 0  # eventual return code when run as script
_PKG_SUBDIR = 'pkg'  # name of directory for package's files
NO_COLOR = os.environ.get('NO_COLOR', False)
def _run_checks(
    try:
        shutil.rmtree(_PKG_SUBDIR)
    except FileNotFoundError:
        pass
    files = _files_in_recipe(recipe, elisp_dir)
    use_default_recipe = files == _files_in_default_recipe(recipe, elisp_dir)
        target = os.path.join(_PKG_SUBDIR, target)
        os.makedirs(os.path.join(_PKG_SUBDIR, os.path.dirname(file)), exist_ok=True)
        subprocess.run(['mv', os.path.join(elisp_dir, file), target])
    if os.environ.get('EXIST_OK', '').lower() != 'true':
        print_related_packages(package_name(recipe))
    print_packaging(files, recipe, use_default_recipe, elisp_dir, clone_address)
    if clone_address and pr_data:
        _print_pr_footnotes(clone_address, pr_data, recipe)
def _return_code(return_code: int = None) -> int:
    _return_code(2)
def check_containerized_build(files: List[str], recipe: str):
    print(f"Building container for {package_name(recipe)}... 🐳")
    if len([file for file in files if file.endswith('.el')]) > 1:
        main_file = os.path.basename(_main_file(files, recipe))
    else:
        main_file = ''  # no need to specify main file if it's the only file
    output = subprocess.run(
        ['make', 'test', f"PACKAGE_MAIN={main_file}"], stdout=subprocess.PIPE,
    ).stdout
    print()
    return sorted(f for f in files if os.path.exists(os.path.join(elisp_dir, f)))


def _files_in_default_recipe(recipe: str, elisp_dir: str) -> list:
    try:
        return _files_in_recipe(_default_recipe(recipe), elisp_dir)
    except ChildProcessError:
        # It is possible that the default recipe is completely invalid and
        # will throw an error -- in that case, just return the empty list:
        return []


def _set_branch(recipe: str, branch_name: str) -> str:
    """Set the branch on the given recipe.
    >>> _set_branch('(abcdef :fetcher hg :url "a/b")', "feature1")
    '(abcdef :fetcher hg :url "a/b" :branch "feature1")'
    """
    tokens = _tokenize_expression(recipe)
    if ':branch' in tokens:
        index = tokens.index(':branch')
        tokens[index + 1] = branch_name
    else:
        tokens.insert(-1, ':branch')
        tokens.insert(-1, f'"{branch_name}"')
    return '(' + ' '.join(tokens[1:-1]) + ')'


def _default_recipe(recipe: str) -> str:
    """Simplify the given recipe, usually to the default.
    # >>> _default_recipe('(recipe :repo a/b :fetcher hg :branch na :files ("*.el"))')
    # '(recipe :repo a/b :fetcher hg :branch na)'
    >>> _default_recipe('(recipe :fetcher hg :url "a/b")')
    '(recipe :url "a/b" :fetcher hg)'
    """
    tokens = _tokenize_expression(recipe)
    fetcher = tokens.index(':fetcher')
    repo_or_url_token = ':repo' if ':repo' in tokens else ':url'
    repo = tokens.index(repo_or_url_token)
    indices = [1, repo, repo + 1, fetcher, fetcher + 1]
    if ':branch' in tokens:
        branch = tokens.index(':branch')
        indices += [branch, branch + 1]
    return '(' + ' '.join(operator.itemgetter(*indices)(tokens)) + ')'
def _tokenize_expression(expression: str) -> List[str]:
    """Turn an elisp expression into a list of tokens.
    tokenized_expression = parsed_expression.split()
def package_name(recipe: str) -> str:
    >>> package_name('(shx :files ...)')
def _main_file(files: List[str], recipe: str) -> str:
    >>> _main_file(['pkg/a.el', 'pkg/b.el'], '(a :files ...)')
    'pkg/a.el'
    name = package_name(recipe)
            if os.path.basename(el) == f"{name}-pkg.el"
            or os.path.basename(el) == f"{name}.el"
def _write_requirements(files: List[str], recipe: str):
        # NOTE: emacs --script <file.el> will set `load-file-name' to <file.el>
        # which can disrupt the compilation of packages that use that variable:
        requirements_el.write('(let ((load-file-name nil))')
        for req in requirements(files, recipe):
        requirements_el.write(') ; end let')
def requirements(
    files: List[str], recipe: str = None, with_versions: bool = False
) -> set:
    reqs = []
    for filename in (f for f in files if os.path.isfile(f)):
        if filename.endswith('-pkg.el'):
    reqs = sum((req.split('(')[1:] for req in reqs), [])
    for ii, req in enumerate(reqs):
        if '"' not in req:
            _fail(f"Version in '{req}' must be a string!  Attempting patch")
            package, version = reqs[ii].split()
            reqs[ii] = f'{package} "{version}"'
    """Pull the requirements out of a -pkg.el file.
    >>> _reqs_from_el_file(io.StringIO(';; package-requires: ((emacs "24.4"))'))
    '((emacs "24.4"))'
        match = re.match('[; ]*Package-Requires:(.*)$', line, re.I)
        if match:
            return match.groups()[0].strip()
def _check_license_github(clone_address: str) -> bool:
    repo_info = repo_info_github(clone_address)
    if not repo_info:
    license_ = repo_info.get('license')
        _note(f"- GitHub API found `{license_.get('name')}`")
            _note('  - Try to use a standard format for your license file.', CLR_WARN)
@functools.lru_cache()
def repo_info_github(clone_address: str) -> dict:
    """What does the GitHub API say about the repo?"""
    if clone_address.endswith('.git'):
        clone_address = clone_address[:-4]
    match = re.search(r'github.com/([^"]*)', clone_address, flags=re.I)
    if not match:
        return {}
    response = requests.get(f"{GITHUB_API}/{match.groups()[0].rstrip('/')}")
    if not response.ok:
        return {}
    return dict(response.json())


def _check_files_for_license_boilerplate(files: List[str]) -> bool:
                '- Please add license boilerplate or an [SPDX-License-Identifier]'
    files: List[str],
    recipe: str,
    use_default_recipe: bool,
    elisp_dir: str,
    clone_address: str = None,
    """Print additional details (how it's licensed, what files, etc.)"""
    _note('### Packaging ###\n', CLR_INFO)
    if clone_address and repo_info_github(clone_address).get('archived'):
        _fail('- GitHub repository is archived')
    _check_recipe(files, recipe, use_default_recipe)
    _print_package_requires(files, recipe)
    _check_license(files, elisp_dir, clone_address)
    print()


def _print_pr_footnotes(clone_address: str, pr_data: dict, recipe: str):
    _note('<!-- ### Footnotes ###', CLR_INFO, highlight='### Footnotes ###')
    repo_info = repo_info_github(clone_address)
    print('```\n' + recipe.replace(' :', '\n  :') + '\n```')  # prettify
    if repo_info:
        if repo_info.get('archived'):
            _fail('- GitHub repository is archived')
        print(f"- Watched: {repo_info.get('watchers_count')}")
        print(f"- Created: {repo_info.get('created_at', '').split('T')[0]}")
        print(f"- Updated: {repo_info.get('updated_at', '').split('T')[0]}")
    print(f"- PR by {pr_data['user']['login']}: {clone_address}")
    if pr_data['user']['login'].lower() not in clone_address.lower():
        _note("- NOTE: Repo and recipe owner don't match", CLR_WARN)
    print('-->\n')


def _check_license(files: List[str], elisp_dir: str, clone_address: str = None):
    repo_licensed = False
    if clone_address:
        repo_licensed = _check_license_github(clone_address)
    if not repo_licensed:
        repo_licensed = _check_repo_for_license(elisp_dir)
    individual_files_licensed = _check_files_for_license_boilerplate(files)
    if not repo_licensed and not individual_files_licensed:
        _fail('- Use a GPL-compatible license.')
        print(
            '  See: https://www.gnu.org/licenses/license-list.en.html#GPLCompatibleLicenses'
        )
def _check_recipe(files: List[str], recipe: str, use_default_recipe: bool):
        _note('- Do not specify :branch except in unusual cases', CLR_WARN)
        # TODO: recipes that do this are failing much higher in the pipeline
        _fail(f"- No .el file matches the name '{package_name(recipe)}'")
    if ':files' in recipe and ':defaults' not in recipe:
        _note('- Prefer the default recipe if possible', CLR_WARN)
        if use_default_recipe:
            _fail(f"  - It is in fact equivalent: `{_default_recipe(recipe)}`")
def _print_package_requires(files: List[str], recipe: str):
    main_requirements = requirements(files, recipe, with_versions=True)
        file_requirements = set(requirements([file], with_versions=True))
def _print_package_files(files: List[str]):
        if not file.endswith('.el'):
            print(f"- {CLR_ULINE}{file}{CLR_OFF} -- not elisp")
            continue
        if file.endswith('-pkg.el'):
            _note(f"- {file} -- consider excluding this; MELPA creates one", CLR_WARN)
            continue
                header = f"{CLR_ERROR}(no header){CLR_OFF}"
                _return_code(2)
            _note('  - Consider excluding this file; MELPA will create one', CLR_WARN)
def print_related_packages(package_name: str):
    known_packages = {
        **_known_packages(),
        **_emacswiki_packages(keywords=[package_name, shorter_name]),
    }
    _note('### Similarly named ###\n', CLR_INFO)
        print(f"- {name}: {known_packages[name]}")
        _fail(f"- Error: a package called '{package_name}' exists", highlight='Error:')
    print()
def _emacswiki_packages(keywords: List[str]) -> dict:
    """Check mirrored emacswiki.org for 'keywords'.
    >>> _emacswiki_packages(keywords=['newpaste'])
    {'newpaste': 'https://github.com/emacsmirror/emacswiki.org/blob/master/newpaste.el'}
    """
    packages = {}
    for keyword in keywords:
        el_file = keyword if keyword.endswith('.el') else (keyword + '.el')
        pkg = f"https://github.com/emacsmirror/emacswiki.org/blob/master/{el_file}"
        if requests.get(pkg).ok:
            packages[keyword] = pkg
    return packages


    """Ask user a yes/no question."""
def check_melpa_recipe(recipe: str):
    """Check a MELPA recipe definition."""
    _return_code(0)
        elisp_dir = os.path.join(elisp_dir, package_name(recipe))
            subprocess.run(['cp', '-r', _local_repo(), elisp_dir])
            _run_checks(recipe, elisp_dir)
            _run_checks(recipe, elisp_dir, clone_address)
def _local_repo() -> str:
def _clone(repo: str, into: str, branch: str, fetcher: str = 'github') -> bool:

    # check if we're being used in GitHub CI -- if so, modify the branch
    if not branch and 'RECIPE' in os.environ:
        branch = (
            os.environ.get('CI_BRANCH', '')
            or os.path.split(os.environ.get('GITHUB_REF', ''))[-1]
            or os.environ.get('TRAVIS_PULL_REQUEST_BRANCH', '')
            or os.environ.get('TRAVIS_BRANCH', '')
        )
        if branch:
            _note(f"CI workflow detected; using branch '{branch}'", CLR_INFO)

    subprocess.run(['mkdir', '-p', into])
        options = ['--branch', branch if branch else 'default']
    result = subprocess.run(git_command, check=True)
    _return_code(0)
        _fail(f"{pr_url} does not appear to be a MELPA PR: {pr_data}")
    if filename != package_name(recipe):
        _fail(f"Recipe filename '{filename}' does not match '{package_name(recipe)}'")
        elisp_dir = os.path.join(elisp_dir, package_name(recipe))
        if _clone(
            clone_address,
            into=elisp_dir,
            branch=_branch(recipe),
            fetcher=_fetcher(recipe),
        ):
            _run_checks(recipe, elisp_dir, clone_address, pr_data)
            assert process.stdin  # pacifies type-checker
@functools.lru_cache()
    name = package_name(recipe)
@functools.lru_cache()
        result = subprocess.run(
            ['emacs', '--batch', '--eval', script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        if result.returncode != 0:
            raise ChildProcessError(result.stderr.decode())
        return result.stdout.decode().strip()
def _check_melpa_pr_loop() -> None:
        if _return_code() != 0:
            _fail('<!-- This PR failed -->')
        else:
            _note('<!-- This PR passed -->')
            print('Watching clipboard for MELPA PR... ', end='\r')
        sys.exit(_return_code())
        check_melpa_recipe(os.environ['RECIPE'])
        sys.exit(_return_code())
            check_melpa_recipe(file.read())
        sys.exit(_return_code())
        _check_melpa_pr_loop()