#include <stdio.h>

#define R 11
#define B  1

main()
{
    int i,j,k,b;

    b = B;
    printf("%d (0.00000,0.00000) 2 %d %d\n", b,        b+1,        b+R);
    printf("%d (0.00000,0.00000) 2 %d %d\n", b+R-1,    b+R-2,      b+2*R-1);
    printf("%d (0.00000,0.00000) 2 %d %d\n", b+(R-1)*R,b+(R-2)*R,  b+(R-1)*R+1);
    printf("%d (0.00000,0.00000) 2 %d %d\n", b+R*R-1,  b+(R-1)*R-1,b+R*R-2);

    printf("\n");
    b = B;
    for(j=1; j<R-1; j++){
	    b++;
	    printf("%d (0.00000,0.00000) 3 %d %d %d\n", b, b-1, b+1, b+R);
    }

    printf("\n");
    b = B;
    for(j=1; j<R-1; j++){
	    b += R;
	    printf("%d (0.00000,0.00000) 3 %d %d %d\n", b, b-R, b+R, b+1);
    }

    printf("\n");
    b = B+(R-1);
    for(j=1; j<R-1; j++){
	    b += R;
	    printf("%d (0.00000,0.00000) 3 %d %d %d\n", b, b-R, b+R, b-1);
    }

    printf("\n");
    b = B+(R-1)*R;
    for(j=1; j<R-1; j++){
	    b++;
	    printf("%d (0.00000,0.00000) 3 %d %d %d\n", b, b-1, b+1, b-R);
    }

    printf("\n");
    for(j=1; j<R-1; j++){
                b = B + j*R;
		for(k=1; k<R-1; k++){
		    b++;
		    printf("%d (0.00000,0.00000) 4 %d %d %d %d\n", 
			    b, b-1, b+1, b-R, b+R);
		}
    }
}
