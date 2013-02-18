from closure_linter import gjslint
import error_rules

if __name__ == '__main__':
    error_rules.InjectErrorReporter()
    gjslint.main()