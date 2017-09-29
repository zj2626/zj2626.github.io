package algorithm;

/**
 * 选择排序
 */
public class BubbleSort {
    public static void main(String args[]) {
        int[] s = new int[]{6, 3, 9, 4, 2, 7, 1, 5};

        for (int k : s) {
            System.out.print(k + "\t");
        }
        System.out.println();

        sort(s);

        for (int k : s) {
            System.out.print(k + "\t");
        }
    }

    private static void sort(int[] s) {
        for (int i = 0; i < s.length - 1; i++) {//表示循环次数
            for (int j = 1; j < s.length - i; j++) {//表示循环位置
                System.out.println(i + "------" + j);
                if (s[j - 1] > s[j]) { //改为 < 则为逆序排序
                    int temp = s[j - 1];
                    s[j - 1] = s[j];
                    s[j] = temp;
                }
            }
        }
    }
}
