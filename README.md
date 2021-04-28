# HOW TO
1. Checkout Romanian UD treebanks [UD_Romanian-RRT](https://github.com/UniversalDependencies/UD_Romanian-RRT) and [UD_Romanian-SiMoNERo](https://github.com/UniversalDependencies/UD_Romanian-SiMoNERo), **in the same folder**.
2. Checkout this repository in the same folder as the above two repositories.
3. Run `python3 fix-all.py <.conllu> file` to apply the corrections. For instance, for the `test` part, run:
`python fix-all.py ..\UD_Romanian-RRT\ro_rrt-ud-test.conllu 2>logs\log-rrt-test-28-04-2021.txt`
