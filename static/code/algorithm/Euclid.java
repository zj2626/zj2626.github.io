package algorithm;

/**
 * 求最大公约数    欧几里得算法
 * <p>
 * 最大公约数（Greatest Common Divisor）缩写为GCD
 * <p>
 * 定理：两个整数的最大公约数等于其中较小的那个数和两数相除余数的最大公约数 -- gcd(a,b) = gcd(b,a mod b)
 * <p>
 * Created by zj on 2017/9/25.
 */
public class Euclid {
    public static void main(String args[]) {
        int a = 31415;
        int b = 14142;

        while (b != 0) {
            int c = a % b;
            a = b;
            b = c;
        }

        System.out.println("最大公约数: " + a);
    }
}
