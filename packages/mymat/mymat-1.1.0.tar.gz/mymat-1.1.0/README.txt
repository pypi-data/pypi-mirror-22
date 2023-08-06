=============
Introduction
=============
This is my module about matrix operation. It imitates matlab grammar.
If you love matlab as well as python, then this is your choice.
It will be a good experience to operating matrices matlab-like.

Sugar: one can use single index to refer to the elements in a matrix. (see following examples)

============
Orgnization
============

mymat
+—— mymat
+—- matshow
+—- matdemo
+—- test_mat
+—— linalg
+—- denoise


============
Feature
============
 
Current Version: 
    1. fix some bugs. 
    2. Demonstrate Gauss elimination with tkinter.
    3. Define LinearEquation class

    import mymat.matdemo
    >>> mymat.matdemo.main()

Main Feature(>0.1.x):
    1. MyMat, PyMat is now the subclass of MatBase
    2. improve some essential methods, fix some bugs
    3. the index can be in reserved order, such as A[3:1:-1,1]
    4. see numerical experiment in mat_demo (improved)
    5. add more methods (introduced below) and A[is,js]=[] now is legal
    6. fix some bugs, make the codes more robust
    finally, another improvement is that when create a matrix, we use following codes to set dtype (may temporarily)

    if data.dtype != np.complex128 and data.dtype != object:
        kwargs.setdefault('dtype', np.float64)

Main Feature(0.0.x):
    1. introduce operator | and & to concatenate matrices
    2. in setitem, the index is allowed to be out of range as matlab with the help of update method (see below)
    3. correct the codes of delete, improve the codes of many method
    4. add poly/expm (Tylor approximation) method to calculate p(A) and e^A
    5. add totex method, transforming a matrix to its tex-form
    6. the default dtype of MyMat is float64(complex128 when it is complex), but the integer matrix is int32. so, don't forget to convert the dtype if neccessary. But this is temporary.

Grammar
=========

basic grammar
---------------

import::

    >>> import mymat
    >>> A = mymat.MyMat([]) # use import mymat.pymat to import PyMat

operators (Python left, Matlab right)::

    A*B := A*B  (B*A := B*A)
    A/B := A/B == A*B.I (B/A := B/A == B*A.I)
    A ** B := A .* B  (B ** A := B .* A)
    A//B := A./B  (B//A := B./A)
    A<<B := A.^B  (B<<A := B.^A)
    A^B := A^B
    A|B := [A,B]   A&B :=[A;B]


We use matlab-type index, instead of python-type index, for example::

    >>> A=TestMat(5)
    [1, 2, 3, 4, 5;
     6, 7, 8, 9, 10;
     11, 12, 13, 14, 15;
     16, 17, 18, 19, 20;
     21, 22, 23, 24, 25]: M(5 X 5)
    >>> A[[3,4,7,10]]    # with single index as in matlab
    [11, 16, 7, 22]: M(1 X 4)
    >>> A[[2,3],1:4]
    [6, 7, 8, 9;
    11, 12, 13, 14]: M(2 X 4)
    >>> A[[1,3],[2,4]]   # use A.get(([1,3],[2,4])) to get matrix([2, 14])
    [2, 4;
    12, 14]: M(2 X 2)

    >>> A[3:1:-1,:]     # reversing order
    [11, 12, 13, 14, 15;
    6, 7, 8, 9, 10;
    1, 2, 3, 4, 5]: M(3 X 5)

Use delete method to delete some rows or columns, as in matlab::

    >>> A=H(7)
    >>> B=A.delete([1,3],slice(3))   #  <=> B=A.copy(); B[[1,3],[1,2,3]]=[]
    >>> B.shape
    (5, 4)

Linear equation::

    >>> le = LinearEquation(A, b)
    >>> print(le.totex())    # print tex of a linear equation


Demonstration and Visualization
---------------------------------

demonstration and numerical experiment::

    >>> import mymat
    >>> import mymat.matdemo        # see Gauss elimination
    >>> A=mymat.MyMat('1,1,1,6;0,4,-1,5;2,-2,1,1')  # or    A=mymat.MyMat('1&1&1&6\\0&4&-1&5\\2&-2&1&1') just copying the latex codes
    >>> mymat.matdemo.guassDemo(A)  # show the process of getting the echelon form of A
    >>> mymat.matdemo.denoiseDemo([n:noised signal(row vector)]) # see a denoising experiment

draw a matrix::

    >>> import mymat.matshow    # draw a matrix on axes(require matplotlib)
    >>> ms = mymat.matshow.MatrixShow(A); ms.show()


Methods and Functions
---------------------

other methods::

    __call__: A(ind) == A[ind]
    delete(ind1=row, ind2=col): delete row-rows and col-columns
    proj(ind1=row, ind2=col): =0 out of A[row, col], for example A.proj(ind1=COLON, ind2=[2,3])=[2,3] where A=[1,2,3,4]
    repmat((ind1, ind2)|ind): repeat matrix as in Matlab (like tile)
    just: cut matrix to a certain size, and supplement zeros if the size is too large.
    cat: as concatenate
    equal: (A == B == C).all()
    apply: A.apply(lambda x:x+1) == A+1
    plus: A.plus(n) == A + nI
    robinson: A.robinson(j, x) == A[j<-x], namely A[:,j]=x used in Cramer rule
    echelon: get the echelon form (include the corresponding column indexes)
    tril, triu, diag are similar to matlab
    row(col)_transform1/2/3: elementary row (column) transforms (Gauss tranforms)
    comat: get the co-matrix (similar with delete)
    cofactor: A.cofactor(i,j)=Aij get the cofactor based on comat
    rho: the spectral radius
    totex: to tex form of matrix
    tolineq: to tex form of linear equations wrt augment matrix
    argmin, argmax


class methods::

    MyMat.zeros, MyMat.ones, MyMat.random, MyMat.randint, MyMat.eye


functions and variables::

    ind2ind: the most essential function
    times: translate single index to double index
    compind: get complementary index (called in proj)
    COLON: slice(None), COLON2=(COLON,COLON)


matrices::

    FM: Fourier matrix
    FIM: Fourier inverse matrix
    FUM: Fourier unitary matrix
    Ho: Horsehold matrix
    Ref: reflection matrix
    H: Hilbert matrix
    Elm1,Elm2,Elm3: elementary matrices (3 types)