package algorithm;

/**
 * 选择排序
 */
public class SelectionSort {
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
        for (int i = 0; i < s.length - 1; i++) {
            for (int j = i + 1; j < s.length; j++) {
                if (s[i] > s[j]) { //改为 < 则为逆序排序
                    int temp = s[i];
                    s[i] = s[j];
                    s[j] = temp;
                }
            }
        }
    }

}
