package dust;

import dust.utils.Tuple;
import lombok.Getter;

import java.util.ArrayList;
import java.util.List;

@Getter
public class Network {
    private final Integer[][] map;
    private final int[][] coverage;

    private final List<Tuple<Integer, Integer>> blackHoles;

    public Network(Integer[][] map) {
        this.map = map;
        this.coverage = new int[map.length][map[0].length];
        this.blackHoles = new ArrayList<>();
        for (int i = 0; i < coverage.length; i++) {
            for (int j = 0; j < coverage[0].length; j++) {
                coverage[i][j] = -1;
                if (map[i][j] == null) {
                    blackHoles.add(new Tuple<>(i, j));
                }
            }
        }
    }

    public Integer getValue(int r, int c) {
        return map[r][c] == null ? Integer.MIN_VALUE : map[r][c];
    }

    public List<Tuple<Integer, Integer>> getBlackHoles() {
        return blackHoles;
    }

    public Integer getValue(int r, int c, int rOffset, int cOffset) {
        var p = getPoint(r, c, rOffset, cOffset);
        return map[p.get_1()][p.get_2()];
    }

    public Tuple<Integer, Integer> getPoint(int r, int c, int rOffset, int cOffset) {
        r += rOffset;
        c += cOffset;

        if (r < 0)
            r = getHeight() - 1;

        if (c < 0)
            c = getWidth() - 1;

        if (r >= getHeight())
            r = r % getHeight();

        if (c >= getWidth())
            c = c % getWidth();

        return new Tuple<>(r, c);
    }

    public int getWidth() {
        return map[0].length;
    }

    public int getHeight() {
        return map.length;
    }

    public boolean isCovered(int i, int j) {
        return coverage[i][j] != -1 || map[i][j] == null; // TODO come gestire i null?
    }

    public void setCovered(int i, int j, int snake) {
        coverage[i][j] = snake;
    }

    public void setUncovered(int i, int j) {
        coverage[i][j] = -1;
    }
}
