package dust;

import dust.utils.Tuple;
import lombok.Getter;

import java.util.ArrayList;
import java.util.List;

@Getter
public class Snake {
    private List<String> segments = new ArrayList<>();
    int consumed = 0;
    int length;

    int index;

    Tuple<Integer, Integer> currentPosition = new Tuple<>(-1, -1);

    public Snake(int index, int length) {
        this.index = index;
        this.length = length;
    }

    public boolean isCompleted() {
        return consumed == length;
    }

    public void moveTo(Tuple<Integer, Integer> point) {
        segments.add(point.get_2() + "");
        segments.add(point.get_1() + "");
        consumed++;
        currentPosition = point;
    }

    public void moveTo(Move move) {
        if (move.getDirection() != null)
            segments.add(move.getDirection());
        else {
            segments.add(move.getPosition().get_2() + "");
            segments.add(move.getPosition().get_1() + "");
        }
        consumed++;
        currentPosition = move.getPosition();
    }

    public void reset() {
        this.consumed = 0;
        segments.clear();
    }
}
