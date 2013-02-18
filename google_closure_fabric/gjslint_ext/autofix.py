from closure_linter import fixjsstyle
import error_rules

if __name__ == '__main__':
    error_rules.InjectErrorReporter()
    fixjsstyle.main()