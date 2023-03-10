package dust;

import lombok.Getter;
import lombok.extern.slf4j.Slf4j;

import java.util.List;

@Slf4j
@Getter
public class InputParser {

    private int columns, rows, numberOfSnakes;

    private Snake[] snakes;

    private Network network;

    public void parseInput(List<String> content) {
        int lineIx = 0;

        // First line
        String line = content.get(lineIx++);
        var parts = line.split(" ");
        columns = Integer.parseInt(parts[0]);
        rows = Integer.parseInt(parts[1]);
        numberOfSnakes = Integer.parseInt(parts[2]);

        // Second line
        snakes = new Snake[numberOfSnakes];
        line = content.get(lineIx++);
        parts = line.split(" ");
        for (int i = 0; i < numberOfSnakes; i++) {
            snakes[i] = new Snake(i, Integer.parseInt(parts[i]));
        }

        // Following R lines
        Integer[][] map = new Integer[rows][columns];
        for (int i = 0; i < rows; i++) {
            line = content.get(lineIx++);
            parts = line.split(" ");
            for (int j = 0; j < columns; j++) {
                if (parts[j].equals("*"))
                    map[i][j] = null;
                else
                    map[i][j] = Integer.parseInt(parts[j]);
            }
        }
        this.network = new Network(map);
    }
}
