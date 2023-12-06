#include <stdio.h>

// Function to calculate the length of an array
int calculateLength(int array[], int arrayLen) {
    return arrayLen;
}

int main() {
    // Example array
    int myArray[] = {1, 2, 3, 4, 5};
    
    // Variable assignment within a for loop
    for (int i = 0; i < 5; i++) {
        int tempVar = myArray[i];
        printf("Value at index %d: %d\n", i, tempVar);
    }

    // Function call with a defined variable
    int length = calculateLength(myArray, 5);
    printf("Length of the array: %d\n", length);

    // Variable with a name containing "Len"
    int arrayLen = 10;
    printf("Array length: %d\n", arrayLen);

    return 0;
}
