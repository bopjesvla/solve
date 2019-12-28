exec > cups.nuxmv
echo MODULE main
echo VAR\ a{1..7}:real\;
echo INIT\ a{1..6}=2
echo INIT a7=4;
echo TRANS "case" a1\>a{2..6}\& "a1>a7 : next(a1) >= a1 - 2; TRUE : next(a1) >= a1; esac"
echo "& case a2 >= a1 &" a2\>a{3..6}\& "a2>a7 : next(a2) >= a2 - 2; TRUE : next(a2) >= a2; esac"
echo "& case" a3\>\=a{1..2}\& a3\>a{4..6}\& "a3>a7 : next(a3) >= a3 - 2; TRUE : next(a3) >= a3; esac"
echo "& case" a4\>\=a{1..3}\& a4\>a{5..6}\& "a4>a7 : next(a4) >= a4 - 2; TRUE : next(a4) >= a4; esac"
echo "& case" a5\>\=a{1..4}\& a5\>a{6..6}\& "a5>a7 : next(a5) >= a5 - 2; TRUE : next(a5) >= a5; esac"
echo "& case" a6\>\=a{1..5}\& "a6>a7 : next(a6) >= a6 - 2; TRUE : next(a6) >= a6; esac"
echo "& case" a7\>\=a{1..5}\& "a7>=a6 : next(a7) >= a7 - 2; TRUE : next(a7) >= a7; esac"
echo TRANS next\(a{1..6}\)+ next\(a7\) = 16
# echo EOF case a<=95 :  next(a) = a + 5;
# echo TRUE : next(a)=a; esac |
# echo case a<=50 :  next(a) = 2*a;
# echo TRUE : next(a)=a; esac
# echo "LTLSPEC G !(" a{1..6}\>\=7\| a7 \>\= 7\)
echo "LTLSPEC G !(" a1 \> 7\)
exec > /dev/tty
nuXmv -source comm.txt cups.nuxmv
