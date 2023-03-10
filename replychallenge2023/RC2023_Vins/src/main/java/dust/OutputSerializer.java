package dust;

import lombok.extern.slf4j.Slf4j;

import java.util.Arrays;
import java.util.Comparator;

@Slf4j
public class OutputSerializer {
    public String serializeOutput(Snake[] input) {
        var sb = new StringBuilder();

        Arrays.sort(input, Comparator.comparing(s -> s.index));

        for (Snake snake : input) {
            if (snake.isCompleted()) {
                for (var segment : snake.getSegments()) {
                    sb.append(segment).append(" ");
                }
                if (!snake.getSegments().isEmpty())
                    sb.setLength(sb.length() - 1);
            }
            sb.append('\n');
        }

        // if (input.length != 0)
        //     sb.setLength(sb.length() - 1);

        return sb.toString();
    }
}
