#include <jni.h>
#include "MathLibrary.h"
#include <stdio.h>

JNIEXPORT jint JNICALL Java_MathLibrary_addNumbers(JNIEnv *env, jobject obj, jint a, jint b) {
    return a - b;  // simple mathematical operation
}

// gcc -fPIC -shared -o libmathlib.so -I${JAVA_HOME}/include -I${JAVA_HOME}/include/linux MathLibrary.c

