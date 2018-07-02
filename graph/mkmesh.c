#include <stdio.h>

#define R 10
#define B  1

main()
{
    int i,j,k,b;

    b = B;
    printf("%d (0.00000,0.00000) 3 %d %d %d\n", b,        b+1,        b+R,        b+R*R);
    printf("%d (0.00000,0.00000) 3 %d %d %d\n", b+R-1,    b+R-2,      b+2*R-1,    b+R-1+R*R);
    printf("%d (0.00000,0.00000) 3 %d %d %d\n", b+(R-1)*R,b+(R-2)*R,  b+(R-1)*R+1,b+(R-1)*R+R*R);
    printf("%d (0.00000,0.00000) 3 %d %d %d\n", b+R*R-1,  b+(R-1)*R-1,b+R*R-2,    b+R*R-1+R*R);
    for(i=1; i<R-1; i++){
        b = B + i*R*R;
        printf("%d (0.00000,0.00000) 4 %d %d %d %d\n", 
			b,        b+1,        b+R,        b-R*R,        b+R*R);
        printf("%d (0.00000,0.00000) 4 %d %d %d %d\n", 
			b+R-1,    b+R-2,      b+2*R-1,    b+R-1-R*R,    b+R-1+R*R);
        printf("%d (0.00000,0.00000) 4 %d %d %d %d\n", 
			b+(R-1)*R,b+(R-2)*R,  b+(R-1)*R+1,b+(R-1)*R-R*R,b+(R-1)*R+R*R);
        printf("%d (0.00000,0.00000) 4 %d %d %d %d\n", 
			b+R*R-1,  b+(R-1)*R-1,b+R*R-2,    b+R*R-1-R*R,  b+R*R-1+R*R);
    }
    b = B + (R-1)*R*R;
    printf("%d (0.00000,0.00000) 3 %d %d %d\n", b,        b+1,        b+R,        b-R*R);
    printf("%d (0.00000,0.00000) 3 %d %d %d\n", b+R-1,    b+R-2,      b+2*R-1,    b+R-1-R*R);
    printf("%d (0.00000,0.00000) 3 %d %d %d\n", b+(R-1)*R,b+(R-2)*R,  b+(R-1)*R+1,b+(R-1)*R-R*R);
    printf("%d (0.00000,0.00000) 3 %d %d %d\n", b+R*R-1,  b+(R-1)*R-1,b+R*R-2,    b+R*R-1-R*R);

    printf("\n");
    b = B;
    for(j=1; j<R-1; j++){
	    b++;
	    printf("%d (0.00000,0.00000) 4 %d %d %d %d\n", b, b-1, b+1, b+R, b+R*R);
    }
    for(i=1; i<R-1; i++){
        b = B + i*R*R;
	for(j=1; j<R-1; j++){
	    b++;
	    printf("%d (0.00000,0.00000) 5 %d %d %d %d %d\n", b, b-1, b+1, b+R, b-R*R, b+R*R);
	}
    }
    b = B + i*R*R;
    for(j=1; j<R-1; j++){
	    b++;
	    printf("%d (0.00000,0.00000) 4 %d %d %d %d\n", b, b-1, b+1, b+R, b-R*R);
    }

    printf("\n");
    b = B+(R-1)*R;
    for(j=1; j<R-1; j++){
	    b++;
	    printf("%d (0.00000,0.00000) 4 %d %d %d %d\n", b, b-1, b+1, b-R, b+R*R);
    }
    for(i=1; i<R-1; i++){
        b = B+(R-1)*R + i*R*R;
	for(j=1; j<R-1; j++){
	    b++;
	    printf("%d (0.00000,0.00000) 5 %d %d %d %d %d\n", b, b-1, b+1, b-R, b-R*R, b+R*R);
	}
    }
    b = B+(R-1)*R + i*R*R;
    for(j=1; j<R-1; j++){
	    b++;
	    printf("%d (0.00000,0.00000) 4 %d %d %d %d\n", b, b-1, b+1, b-R, b-R*R);
    }

    printf("\n");
    b = B;
    for(j=1; j<R-1; j++){
	    b += R;
	    printf("%d (0.00000,0.00000) 4 %d %d %d %d\n", b, b-R, b+R, b+1, b+R*R);
    }
    for(i=1; i<R-1; i++){
	    b = B + i*R*R;
    	    for(j=1; j<R-1; j++){
	    	b += R;
	    	printf("%d (0.00000,0.00000) 5 %d %d %d %d %d\n", b, b-R, b+R, b+1, b-R*R, b+R*R);
    	    }
    }
    b = R + i*R*R;
    for(j=1; j<R-1; j++){
    	    b += R;
    	    printf("%d (0.00000,0.00000) 4 %d %d %d %d\n", b, b-R, b+R, b+1, b-R*R);
    }

    printf("\n");
    b = B+(R-1);
    for(j=1; j<R-1; j++){
	    b += R;
	    printf("%d (0.00000,0.00000) 4 %d %d %d %d\n", b, b-R, b+R, b-1, b+R*R);
    }
    for(i=1; i<R-1; i++){
	    b = B+(R-1) + i*R*R;
    	    for(j=1; j<R-1; j++){
	    	b += R;
	    	printf("%d (0.00000,0.00000) 5 %d %d %d %d %d\n", b, b-R, b+R, b-1, b-R*R, b+R*R);
    	    }
    }
    b = R+(R-1) + i*R*R;
    for(j=1; j<R-1; j++){
    	    b += R;
    	    printf("%d (0.00000,0.00000) 4 %d %d %d %d\n", b, b-R, b+R, b-1, b-R*R);
    }

    printf("\n");
    for(j=1; j<R-1; j++){
                b = B + j*R;
		for(k=1; k<R-1; k++){
		    b++;
		    printf("%d (0.00000,0.00000) 5 %d %d %d %d %d\n", 
			    b, b-1, b+1, b-R, b+R, b+R*R);
		}
    }
    for(i=1; i<R-1; i++){
	    for(j=1; j<R-1; j++){
                b = B + i*R*R + j*R;
		for(k=1; k<R-1; k++){
		    b++;
		    printf("%d (0.00000,0.00000) 6 %d %d %d %d %d %d\n", 
			    b, b-1, b+1, b-R, b+R, b-R*R, b+R*R);
		}
	    }
    }
    for(j=1; j<R-1; j++){
                b = B + i*R*R + j*R;
		for(k=1; k<R-1; k++){
		    b++;
		    printf("%d (0.00000,0.00000) 5 %d %d %d %d %d\n", 
			    b, b-1, b+1, b-R, b+R, b-R*R);
		}
    }
}
