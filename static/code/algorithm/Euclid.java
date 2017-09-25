package algorithm;

/**
 * 求最大公约数      欧几里得算法
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
