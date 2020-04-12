import configparser
    recipe: str,  # e.g. of the form (my-package :repo ...)
    check_containerized_build(files, recipe)
    print_related_packages(recipe)
    """Return (and optionally set) the current return code.
    """Validate whether the recipe looks correct.
    >>> validate_recipe('(abc :repo "xyz" :fetcher github) ; abc recipe!')
def check_containerized_build(files: list, recipe: str):
    package_name = _package_name(recipe)
    main_file = os.path.basename(_main_file(files, recipe))
    output = subprocess.check_output(['make', 'test', f"PACKAGE_MAIN={main_file}"])
    files = run_build_script(
    """Hacky function to turn an elisp expression into a list of tokens.
        parsed_expression = run_build_script(
    """Return the package's name, based on the recipe.
    return _tokenize_expression(recipe)[1]
def _main_file(files: list, recipe: str) -> str:
    """Figure out the 'main' file of the recipe, per MELPA convention.
            for el in sorted(files)
def _write_requirements(files: list, recipe: str):
        for req in _requirements(files, recipe):
            if req == 'org':
                # TODO: is there a cleaner way to install a recent version of org?!
                requirements_el.write(
                    "(package-install (cadr (assq 'org package-archive-contents)))"
                )
            elif req != 'emacs':
def _requirements(files: list, recipe: str = None, with_versions: bool = False) -> set:
        main_file = _main_file(files, recipe)
            files = [main_file]
    for filename in files:
    """Hacky function to pull the requirements out of a -pkg.el file.
    """Hacky function to pull the requirements out of an elisp file.
def check_license(files: list, elisp_dir: str, clone_address: str = None):
        repo_licensed = _check_repo_for_license(elisp_dir)
    individual_files_licensed = _check_files_for_license_boilerplate(files)
    """Use the GitHub API to check for a license."""
    _fail('- Use a LICENSE file that GitHub can detect (e.g. no markup) if possible')
def _check_repo_for_license(elisp_dir: str) -> bool:
                print(f"<!-- {license_} excerpt: `{stream.readline().strip()}...` -->")
def _check_files_for_license_boilerplate(files: list) -> bool:
    """Check a list of elisp files for license boilerplate."""
    for file in files:
        if not file.endswith('.el') or file.endswith('-pkg.el'):
        with open(file) as stream:
            license_ = _check_file_for_license_boilerplate(stream)
        basename = os.path.basename(file)
            _fail(
                '- Please add license boilerplate or an [SPDX license identifier]'
                '(https://spdx.org/using-spdx-license-identifier)'
                f" to {basename}"
            )
def _check_file_for_license_boilerplate(el_file: TextIO) -> str:
    """Check an elisp file for some license boilerplate.
    >>> _check_file_for_license_boilerplate(io.StringIO('SPDX-License-Identifier:  ISC '))
    'ISC'
    >>> _check_file_for_license_boilerplate(io.StringIO('GNU General Public License'))
    'GPL'
    """
    text = el_file.read()
    # SPDX license identifiers are easy https://spdx.org/using-spdx-license-identifier
    match = re.search('SPDX-License-Identifier:[ ]+(.*)', text, flags=re.I)
    if match:
        return match.groups()[0].strip()
    # otherwise, look for fingerprints (consider <https://github.com/emacscollective/elx>)
    fingerprints = [
        ('Unlicense', 'This is free and unencumbered software released into'),
        ('Apache 2.0', 'Licensed under the Apache License, Version 2.0'),
        ('BSD 3-Clause', 'Redistribution and use in source and binary forms'),
    for license_key, license_text in fingerprints:
        if re.search(license_text, text):
    recipe: str, files: list, pr_data: dict = None, clone_address: str = None
    _print_recipe(files, recipe)
    _print_requirements(files, recipe)
    _print_package_files(files)
def _print_recipe(files: list, recipe: str):
    if not _main_file(files, recipe):
def _print_requirements(files: list, recipe: str):
    main_requirements = _requirements(files, recipe, with_versions=True)
    for file in files:
                f"{os.path.basename(_main_file(files, recipe))}!"
def _print_package_files(files: list):
    for file in files:
        if os.path.isdir(file):
            print(f"- {CLR_ULINE}{file}{CLR_OFF} -- directory")
        with open(file) as stream:
            print(
                f"- {CLR_ULINE}{file}{CLR_OFF}"
                f" ({_check_file_for_license_boilerplate(stream) or 'unknown license'})"
                + (f" -- {header}" if header else "")
            )
        if file.endswith('-pkg.el'):
    """Print list of potentially related packages."""
    package_name = _package_name(recipe)
    shorter_name = package_name[:-5] if package_name.endswith('-mode') else package_name
    known_packages = _known_packages()
    known_names = [name for name in known_packages if shorter_name in name]
    if not known_names:
        return
    _note('\n### Similarly named packages ###\n', CLR_INFO)
    for name in known_names[:10]:
        print(f"- {name} {known_packages[name]}")
    if package_name in known_packages:
        _fail(f"- {package_name} {known_packages[package_name]} is in direct conflict")
def _known_packages() -> dict:
    melpa_packages = {
        package: f"https://melpa.org/#/{package}"
    epkgs = 'https://raw.githubusercontent.com/emacsmirror/epkgs/master/.gitmodules'
    epkgs_parser = configparser.ConfigParser()
    epkgs_parser.read_string(requests.get(epkgs).text)
    epkgs_packages = {
        epkg.split('"')[1]: 'https://' + data['url'].replace(':', '/')[4:]
        for epkg, data in epkgs_parser.items()
        if epkg != 'DEFAULT'
    }
    return {**epkgs_packages, **melpa_packages}
        if _clone(clone_address, into=elisp_dir, branch=_branch(recipe), scm=scm):
def _clone(repo: str, into: str, branch: str = None, scm: str = 'git') -> bool:
    print(f"Checking out {repo}")
        _fail(f"Unable to locate {repo}")
    if scm == 'git':
        # MELPA recipe must specify the branch using the :branch keyword
        options = ['--branch', branch if branch else 'master']
        options += ['--depth', '1', '--single-branch']
        options = ['--branch', branch] if branch else []
    git_command = [scm, 'clone', *options, repo, into]
    if result.returncode != 0:
    """Determine the source code manager used (mercurial or git).
    """Return the recipe's branch if available, else the empty string.
        _fail(f"{pr_url} does not appear to be a MELPA PR")
    if filename != _package_name(recipe):
        _fail(f"Filename '{filename}' does not match '{_package_name(recipe)}'")
        return
        if _clone(clone_address, into=elisp_dir, branch=_branch(recipe)):
            run_checks(recipe, elisp_dir, clone_address, pr_data)
    """Fetch the upstream repository URL for the recipe.
    return run_build_script(
    """Turn the recipe into a serialized 'package-recipe' object."""
        with open(os.path.join(tmpdir, name), 'w') as file:
            file.write(recipe)
        return run_build_script(
def run_build_script(script: str) -> str:
    """Run an elisp script in a package-build context.
    >>> run_build_script('(send-string-to-terminal "Hello world")')
    'Hello world'
    """
        with open(os.environ['RECIPE_FILE'], 'r') as file:
            check_recipe(file.read())