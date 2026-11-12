
// C++ code to demonstrate sorting of a 
// 2D vector on basis of a column 
#include<iostream> 
#include<vector> // for 2D vector 
#include<algorithm> // for sort() 
using namespace std; 
  
// Driver function to sort the 2D vector 
// on basis of a particular column 
bool sortcol( const vector<int>& v1, 
               const vector<int>& v2 ) { 
 return v1[1] < v2[1]; 
} 
  
int main() 
{ 
    // Initializing 2D vector "vect" with 
    // values 
    vector< vector<int> > vect{{3, 5, 1}, 
                                {4, 8, 6}, 
                                {7, 2, 9}}; 
  
    // Number of rows; 
    int m = vect.size(); 
  
    // Number of columns (Assuming all rows 
    // are of same size).  We can have different 
    // sizes though (like Java). 
    int n = vect[0].size(); 
      
    // Displaying the 2D vector before sorting 
    cout << "The Matrix before sorting is:\n"; 
    for (int i=0; i<m; i++) 
    { 
        for (int j=0; j<n ;j++) 
            cout << vect[i][j] << " "; 
        cout << endl; 
    }                                
  
    // Use of "sort()" for sorting on basis 
    // of 2nd column 
    sort(vect.begin(), vect.end(),sortcol); 
  
    // Displaying the 2D vector after sorting 
    cout << "The Matrix after sorting is:\n"; 
    for (int i=0; i<m; i++) 
    { 
        for (int j=0; j<n ;j++) 
            cout << vect[i][j] << " "; 
        cout << endl; 
    } 
    return 0; 
} 



/******************************************************************************

                              Online C++ Compiler.
               Code, Compile, Run and Debug C++ program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/

#include <iostream>

using namespace std;
#include <iostream>

using namespace std;

int main()
{
    cout<<"Hello World";
    float M[2][2],tm[1][2];
    M[0][0]=1;
    M[0][1]=2;
    M[1][0]=3;
    M[1][1]=4;
    
    for (size_t  i= 0; i < 2; i++){
        for (size_t  j= 0; j < 2; j++){
        cout<< " ";
        cout<<M[i][j]; 
        cout<< " ";    
        }
    }
    
     
    for (size_t  i= 0; i < 2; i++){
        for (size_t  j= 0; j < 2; j++){
            if(M[i][1]>M[j][1]){
            tm[0][0]=M[0][0];
            tm[0][1]=M[0][1];
            M[0][0] =M[1][0];
            M[0][1] =M[1][1];
            M[1][0]= tm[0][0];   
            M[1][1]= tm[0][1];
            }
          
        }
    }
    
    for (size_t  i= 0; i < 2; i++){
        for (size_t  j= 0; j < 2; j++){
        cout<< " ";
        cout<<M[i][j]; 
        cout<< " ";    
        }
    }
    
    
} 

int main()
{
    cout<<"Hello World";
    float M[3][2],tm[1][2];
    M[0][0]=1;
    M[0][1]=2;
    M[1][0]=3;
    M[1][1]=4;
    M[2][0]=5;
    M[2][1]=6;
    
    
    for (size_t  i= 0; i < 3; i++){
        for (size_t  j= 0; j < 2; j++){
        cout<< " ";
        cout<<M[i][j]; 
        cout<< " ";    
        }
    }
    
     
    for (size_t  i= 0; i < 3; i++){
        for (size_t  j= 0; j < 2; j++){
            if(M[i][1]>M[j][1]){
            tm[0][0]=M[0][0];
            tm[0][1]=M[0][1];
            M[0][0] =M[1][0];
            M[0][1] =M[1][1];
            M[1][0]= tm[0][0];   
            M[1][1]= tm[0][1];
            }
          
        }
    }
    
    for (size_t  i= 0; i < 3; i++){
        for (size_t  j= 0; j < 2; j++){
        cout<< " ";
        cout<<M[i][j]; 
        cout<< " ";    
        }
    }

  // The best code ever
   cout<<"Hello World";
    float M[3][2],tm[1][2];
    M[0][0]=50;
    M[0][1]=50;
    M[1][0]=60;
    M[1][1]=60;
    M[2][0]=30;
    M[2][1]=30;
    
    
    for (size_t  i= 0; i < 3; i++){
        for (size_t  j= 0; j < 2; j++){
        cout<< " ";
        cout<<M[i][j]; 
        cout<< " ";    
        }
    }
    
     
    for (size_t  i= 0; i < 3; i++){
        for (size_t  j= 0; j < 2; j++){
            if(M[i][1]<M[j][1]){
            tm[0][0]=M[i][0];
            tm[0][1]=M[i][1];
            M[i][0] =M[j][0];
            M[i][1] =M[j][1];
            M[j][0]= tm[0][0];   
            M[j][1]= tm[0][1];
            }
          
        }
    }
    
    for (size_t  i= 0; i < 3; i++){
        for (size_t  j= 0; j < 2; j++){
        cout<< " ";
        cout<<M[i][j]; 
        cout<< " ";    
        }
    }  

    int main()
{
     cout<<"Hello World";
    float M[3][2],tm[1][2];
    M[0][0]=50;
    M[0][1]=50;
    M[1][0]=0;
    M[1][1]=2;
    M[2][0]=30;
    M[2][1]=30;
    
    
    for (size_t  i= 0; i < 3; i++){
        for (size_t  j= 0; j < 2; j++){
        cout<< " \n";
        cout<< "Element ("<<i<<j<<")=" <<M[i][j]; 
        cout<< " \n";    
        }
    }
    
     
    for (size_t  i= 0; i < 3; i++){
        for (size_t  j= 0; j < 2; j++){
            if(M[i][1]<M[j][1]){
            tm[0][0]=M[i][0];
            tm[0][1]=M[i][1];
            M[i][0] =M[j][0];
            M[i][1] =M[j][1];
            M[j][0]= tm[0][0];   
            M[j][1]= tm[0][1];
            }
          
        }
    }
    
    for (size_t  i= 0; i < 3; i++){
        for (size_t  j= 0; j < 2; j++){
        cout<< " ";
        cout<<M[i][j]; 
        cout<< " ";    
        }
    }
}

// WORKING CODE FINALLY
int main()
{
    cout<<"Hello World";
    int cl=4;
    float f_matrix[cl][5], tm[1][5],x=10.0;

    for (size_t  i= 0; i < cl; i++){
        for (size_t  j= 0; j < 5; j++){
        f_matrix[i][j]=x;
        x=x+i-j;
        }
    } 
    
    
      //Display the input matrix
    for (size_t  i= 0; i < cl; i++){
        for (size_t  j= 0; j < 5; j++){
        cout<< " \n";
        cout<< "Element_IN("<<i<<j<<")=" <<f_matrix[i][j];
        cout<< " \n";
        }
    }

        for (size_t i = 0; i < cl; i++)
    {
        for (size_t j = 0; j < cl; j++)
        {
            if (f_matrix[i][2] < f_matrix[j][2])
            {
                tm[0][0] = f_matrix[i][0];
                tm[0][1] = f_matrix[i][1];
                tm[0][2] = f_matrix[i][2];
                tm[0][3] = f_matrix[i][3];
                tm[0][4] = f_matrix[i][4];
                f_matrix[i][0] = f_matrix[j][0];
                f_matrix[i][1] = f_matrix[j][1];
                f_matrix[i][2] = f_matrix[j][2];
                f_matrix[i][3] = f_matrix[j][3];
                f_matrix[i][4] = f_matrix[j][4];
                f_matrix[j][0] = tm[0][0];
                f_matrix[j][1] = tm[0][1];
                f_matrix[j][2] = tm[0][2];
                f_matrix[j][3] = tm[0][3];
                f_matrix[j][4] = tm[0][4];     
            }
        }
}

   for (size_t  i= 0; i < cl; i++){
        for (size_t  j= 0; j < 5; j++){
        cout<< " \n";
        cout<< "Element_OUT ("<<i<<j<<")=" <<f_matrix[i][j];
        cout<< " \n";
        }
    }
}




#include <iostream>
#include <vector>
 
#define M 3
#define N 4
 
int main()
{ extern std::vector<std::vector<float>> mc(int n, int m);
  std::vector<std::vector<float>> MAT;
  int m=3,n=5;
  MAT=mc(m,n);
  std::cout << MAT[1][1] << std::endl;
  MAT[1][1]=30.5;
  std::cout << MAT[1][1] << std::endl;
  for(size_t i=0;i<m;i++){
      for(size_t j=0;j<n;j++){
        MAT[i][j]=i;  
      }
  }
  std::cout << MAT[m-1][n-1] << std::endl;
    
   
    return 0;
}

 std::vector<std::vector<float>> mc(int n, int m){
     // specify default value to fill the vector elements
    int default_value = 1;
 
    // first initialize a vector of ints with given default value
    std::vector<float> v(m,0);
 
    // Use above vector to initialize the two-dimensional vector
    // using the fill constructor
    std::vector<std::vector<float>> matrix(n, v);
 
    // print the two-dimensional vector
    return matrix;
    
}

//===================================================

#include <iostream>
#include <vector>

 
int main()
{ extern std::vector<std::vector<float>> mc(int n, int m);
  std::vector<std::vector<float>> MAT;
  int m=3,n=5;
  MAT=mc(m,n);
  //std::cout << MAT[1][1] << std::endl;
  MAT[1][1]=30.5;
  //std::cout << MAT[1][1] << std::endl;
  for(size_t i=0;i<MAT.size();i++){
      for(size_t j=0;j<MAT[i].size();j++){
        MAT[i][j]=i;  
      }
  }
  //size_t x=MAT.size)();
  //std::cout <<  x<< std::endl;
  
   
   
    return 0;
}





std::vector<std::vector<float> > mc(int n, int m){
     // specify default value to fill the vector elements
    int default_value = 1;
 
    // first initialize a vector of ints with given default value
    std::vector<float> v(n,50);
 
    // Use above vector to initialize the two-dimensional vector
    // using the fill constructor
    std::vector<std::vector<float> > M(m, v);
    
    //M[1][1]=5;
    // print the two-dimensional vector

    for (int i = 0; i < M.size(); i++){
    
    for (int j = 0; j < M[i].size(); j++)
       {
           std::cout<< M[i][j] << " "<< std::endl;
       }   
         
    }
    return M;
}


//======================================================the most perfect

#include <iostream>
#include <vector>

 
int main()
{ extern std::vector<std::vector<float>> mc(int n, int m);
  std::vector<std::vector<float>> MAT;
  int m=3,n=5;
  MAT=mc(m,n);
  //std::cout << MAT[1][1] << std::endl;
  MAT[1][1]=30.5;
  //std::cout << MAT[1][1] << std::endl;
  for(size_t i=0;i<MAT.size();i++){
      for(size_t j=0;j<MAT[i].size();j++){
        MAT[i][j]=i;  
      }
  }
  //size_t x=MAT.size)();
  //std::cout <<  x<< std::endl;
  
   
   
    return 0;
}





std::vector<std::vector<float> > mc(int n, int m){
     // specify default value to fill the vector elements
    int default_value = 1;
 
    // first initialize a vector of ints with given default value
    std::vector<float> v(n,50);
 
    // Use above vector to initialize the two-dimensional vector
    // using the fill constructor
    std::vector<std::vector<float> > M(m, v);
    
    //M[1][1]=5;
    // print the two-dimensional vector

    for (int i = 0; i < M.size(); i++){
    
    for (int j = 0; j < M[i].size(); j++)
       {
           std::cout<< M[i][j] << ' ' ;
          
       }   
          std::cout << std::endl;
    }
    return M;
}

///////////////////////////////this one is working ;) 

#include <iostream>
#include <vector>

 
int main()
{ extern std::vector<std::vector<float>> mc(int n, int m);
  std::vector<std::vector<float>> MAT;
  int m=3,n=5;
  MAT=mc(m,n);
  //std::cout << MAT[1][1] << std::endl;
  //MAT[1][1]=30.5;
  //std::cout << MAT[1][1] << std::endl;
  ///for(size_t i=0;i<MAT.size();i++){
   //   for(size_t j=0;j<MAT[i].size();j++){
  //      MAT[i][j]=i;  
   //   }
  //}
  //size_t x=MAT.size)();
  //std::cout <<  x<< std::endl;
  
   
   
    return 0;
}





std::vector<std::vector<float> > mc(int m, int n){
     // specify default value to fill the vector elements
    int default_value = 1;
 
    // first initialize a vector of ints with given default value
    std::vector<float> v(n,0);
 
    // Use above vector to initialize the two-dimensional vector
    // using the fill constructor
    std::vector<std::vector<float> > M(m, v);
    
    //M[1][1]=5;
    // print the two-dimensional vector

    for (int i = 0; i < M.size(); i++){
    
    for (int j = 0; j < M[i].size(); j++)
       {   M[i][j]=i-j;
           std::cout<< M[i][j] << ' ' ;
          
       }   
          std::cout << std::endl;
    }
    
    //float tm[1][5];
    std::vector<float> tm(n,0);
    for (int i = 0; i < M.size(); i++){
    
    for (int j = 0; j < M.size(); j++)
       {  
           if (M[i][2] >= M[j][2])
            {
                tm[0] = M[i][0];
                tm[1] = M[i][1];
                tm[2] = M[i][2];
                tm[3] = M[i][3];
                tm[4] = M[i][4];
                M[i][0] = M[j][0];
                M[i][1] = M[j][1];
                M[i][2] = M[j][2];
                M[i][3] = M[j][3];
                M[i][4] = M[j][4];
                M[j][0] = tm[0];
                M[j][1] = tm[1];
                M[j][2] = tm[2];
                M[j][3] = tm[3];
                M[j][4] = tm[4]; 
           } 
          
       }   
          
    }
    
        for (int i = 0; i < M.size(); i++){
    
    for (int j = 0; j < M[i].size(); j++)
       {   M[i][j]=i-j;
           std::cout<< M[i][j] << ' ' ;
          
       }   
          std::cout << std::endl;
    }
    
    
    
    
    return M;
}