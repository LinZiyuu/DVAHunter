from util import test_step1, test_step2, test_step3


# TODO 通过(Df, Dt, Ut)
# TODO 进行三个测试

def fronting_tester(Df, Dt, Ut):
    print(f"Testing: Df:{Df}, Dt:{Dt}, Ut:{Ut}")
    rt = test_step1(dt=Dt, uri=Ut) 
    rv = test_step2(df=Df, dt=Dt, uri=Ut)
    rf = test_step3(df=Df, uri=Ut)
    if rt == rv and rv != rf:
        print(f"Domain Fronting: Df:{Df}, Dt:{Dt}, Ut:{Ut}")
        return (Df, Dt, Ut)
    else:
        return()
