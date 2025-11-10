public class MathLibrary {
    // Declare native method
    public native int addNumbers(int a, int b);

    // Load the shared library
    static {
        System.loadLibrary("mathlib");
    }

    // Main method to test
    public static void main(String[] args) {
        MathLibrary m = new MathLibrary();
        int result = m.addNumbers(10, 20);
        System.out.println("Sum from native library: " + result);
    }
}

// javac MathLibrary.java
// javac -h . MathLibrary.java
// gcc -shared -o libmathlib.so -I${JAVA_HOME}/include -I${JAVA_HOME}/include/linux MathLibrary.c
// java -Djava.library.path=. MathLibrary