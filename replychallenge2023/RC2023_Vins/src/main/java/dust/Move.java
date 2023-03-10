package dust;


import dust.utils.Tuple;
import lombok.Data;

@Data
public class Move {
    final String direction;
    final Tuple<Integer, Integer> position;

    public Move(String direction, Tuple<Integer, Integer> position) {
        this.direction = direction;
        this.position = position;
    }
}
