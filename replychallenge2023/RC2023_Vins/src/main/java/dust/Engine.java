package dust;

import dust.utils.Tuple;
import lombok.extern.slf4j.Slf4j;

import java.util.*;

@Slf4j
public class Engine {
    private Network network;
    private Snake[] snakes;

    private LinkedList<Tuple<Integer, Integer>> queue = new LinkedList<>();

    public Engine(Network network, Snake[] snakes) {
        this.network = network;
        this.snakes = snakes;
    }

    private void initQueue() {
        Tuple<Integer, Integer>[] positions = new Tuple[network.getWidth() * network.getHeight()];
        for (int i = 0; i < network.getHeight(); i++) {
            for (int j = 0; j < network.getWidth(); j++) {
                positions[i * network.getWidth() + j] = new Tuple<>(i, j);
            }
        }
        Arrays.sort(positions, Comparator.comparing(t -> network.getValue(t.get_1(), t.get_2())));
        for (int i = positions.length - 1; i >= 0; i--) {
            queue.addLast(positions[i]);
        }
    }

    private void initSnakes() {
        Arrays.sort(snakes, Comparator.comparing(s -> -s.length));
    }

    public void start() {
        log.debug("Engine started");

        initQueue();
        initSnakes();

        for (int i = 0; i < snakes.length; i++) {
            var snake = snakes[i];

            LinkedList<Tuple<Integer, Integer>> toReadd = new LinkedList<>();
            int maxTries = 20;
            while (maxTries > 0) {
                maxTries--;
                var point = findStartingPointQueue(snake);
                if (point == null)
                    break;
                toReadd.addLast(point);
                var moves = new LinkedList<Move>();

                moves.addLast(new Move(null, point));
                snake.moveTo(point);
                network.setCovered(point.get_1(), point.get_2(), snake.getIndex());

                while (!snake.isCompleted()) {
                    var currentMoves = findNextFirst(snake);
                    if (currentMoves == null || currentMoves.isEmpty())
                        break;
                    for (var m : currentMoves) {
                        moves.addLast(m);
                        snake.moveTo(m);
                        network.setCovered(m.getPosition().get_1(), m.getPosition().get_2(), snake.getIndex());
                    }
                }

                int score = moves.parallelStream().filter(m -> Integer.MIN_VALUE != network.getValue(m.getPosition().get_1(), m.getPosition().get_2())).mapToInt(m -> network.getValue(m.getPosition().get_1(), m.getPosition().get_2())).sum();

                if ((snake.isCompleted() && score > 0) || queue.isEmpty()) {
                    break;
                } else {
                    snake.reset();
                    for (var move : moves) {
                        network.setUncovered(move.getPosition().get_1(), move.getPosition().get_2());
                    }
                }
            }

            if (!snake.isCompleted()) {
                snake.reset();
                while (!toReadd.isEmpty()) {
                    queue.addFirst(toReadd.removeLast());
                }
            }
        }
    }

    Tuple<Integer, Integer> findStartingPointQueue(Snake snake) {
        while (!queue.isEmpty()) {
            var first = queue.removeFirst();
            if (!network.isCovered(first.get_1(), first.get_2())) {
                return first;
            }
        }
        return null;
    }


    Tuple<Integer, Integer> findStartingPointFirst(Snake snake) {
        for (int i = 0; i < network.getHeight(); i++) {
            for (int j = 0; j < network.getWidth(); j++) {
                if (!network.isCovered(i, j)) {
                    return new Tuple<>(i, j);
                }
            }
        }
        return null;
    }

    static Object[][] offsets = new Object[][]{
            {"D", 1, 0},
            {"L", 0, -1},
            {"R", 0, 1},
            {"U", -1, 0}
    };

    List<Move> findNextMove(Snake snake) {
        var currentPos = snake.getCurrentPosition();
        List<Move> newPos = new ArrayList<>(2);
        int max = Integer.MIN_VALUE;
        for (int i = 0; i < offsets.length; i++) {
            var offset = offsets[i];
            var tmp = network.getPoint(currentPos.get_1(), currentPos.get_2(), (int) offset[1], (int) offset[2]);
            int newVal = network.getValue(tmp.get_1(), tmp.get_2());
            if (!network.isCovered(tmp.get_1(), tmp.get_2())) {
                if (newVal > max) {
                    newPos.clear();
                    newPos.add(new Move((String) offset[0], tmp));
                    max = newVal;
                }
            } else if (newVal == Integer.MIN_VALUE && (snake.getConsumed() + 3 <= snake.getLength())) { // buco nero
                for (var bh : network.getBlackHoles()) {
                    if (bh.equals(tmp))
                        continue;
                    for (int j = 0; j < offsets.length; j++) {
                        var offset2 = offsets[j];
                        var tmp2 = network.getPoint(bh.get_1(), bh.get_2(), (int) offset2[1], (int) offset2[2]);
                        int newVal2 = network.getValue(tmp2.get_1(), tmp2.get_2());
                        if (!network.isCovered(tmp2.get_1(), tmp2.get_2())) {
                            if (newVal2 > max) {
                                newPos.clear();
                                newPos.add(new Move((String) offset[0], tmp));
                                newPos.add(new Move(null, bh));
                                newPos.add(new Move((String) offset2[0], tmp2));
                                max = newVal2;
                            }
                        }
                    }
                }
            }
        }
        return newPos;
    }

    List<Move> findNextFirst(Snake snake) {
        var currentPos = snake.getCurrentPosition();
        List<Move> newPos = new ArrayList<>(2);
        for (int i = 0; i < offsets.length; i++) {
            var offset = offsets[i];
            var tmp = network.getPoint(currentPos.get_1(), currentPos.get_2(), (int) offset[1], (int) offset[2]);
            int newVal = network.getValue(tmp.get_1(), tmp.get_2());
            if (!network.isCovered(tmp.get_1(), tmp.get_2())) {
                newPos.clear();
                newPos.add(new Move((String) offset[0], tmp));
            } else if (newVal == Integer.MIN_VALUE) { // buco nero
                for (var bh : network.getBlackHoles()) {
                    if (bh.equals(tmp))
                        continue;
                    for (int j = 0; j < offsets.length; j++) {
                        var offset2 = offsets[j];
                        var tmp2 = network.getPoint(bh.get_1(), bh.get_2(), (int) offset2[1], (int) offset2[2]);
                        if (!network.isCovered(tmp2.get_1(), tmp2.get_2())) {
                            newPos.clear();
                            newPos.add(new Move((String) offset[0], tmp));
                            newPos.add(new Move(null, bh));
                            newPos.add(new Move((String) offset2[0], tmp2));
                            break;
                        }
                    }
                }
            }
        }
        return newPos;
    }

}
