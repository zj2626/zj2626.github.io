package algorithm;

/**
 * 求素数    埃拉托色尼筛选法
 * Created by zj on 2017/9/25.
 */
public class PrimeNumber {
    public static void main(String args[]) {
        int n = 100;
        int[] num = new int[n];

        for (int i = 2; i < 100; i++) {
            num[i] = i;
        }

        for (int i = 2; i < Math.sqrt(n); i++) {
            for (int j = i + 1; j < n; j++) {
                if (num[j] != 0 && j % i == 0) {
                    num[j] = 0;
                }
            }
        }

        for (int i = 0; i < 100; i++) {
            if (num[i] != 0)
                System.out.print(num[i] + "\t");
        }
    }
}
