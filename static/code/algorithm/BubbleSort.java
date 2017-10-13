package algorithm;

/**
 * 选择排序
 */
public class BubbleSort {
    public static void main(String args[]) {
        int[] s = new int[]{6, 3, 9, 4, 2, 7, 1, 5, 10, 11, 15};

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
        int flag = 0;

        for (int i = 0; i < s.length - 1; i++) {//表示循环次数
            for (int j = 1; j < s.length - i; j++) {// 每次循环把j位置的值与(j-1)的值比较, 把最小(大)的移动到j的位置(即交换位置)
                if (s[j - 1] > s[j]) { //改为 < 则为逆序排序
                    int temp = s[j - 1];
                    s[j - 1] = s[j];
                    s[j] = temp;
                    flag = 1;
                }
            }

            //判断当某次冒泡排序时没有进行位置移动,则说明已经完全按照所求的顺序进行排列了, 则不需要再进行后序的冒泡了
            if (flag == 0)
                break;
            else
                flag = 0;
        }
    }
}
