package dust.utils;

import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;

@Slf4j
public final class IOHelper {
    private IOHelper() {
    }

    @SneakyThrows
    public static void write(File file, String content) {
        Files.writeString(file.toPath(), content);
    }

    @SneakyThrows
    public static List<String> read(File file) {
        return Files.readAllLines(file.toPath());
    }

    public static List<File> getFilesInDirectory(String path) {
        return Arrays.stream(Objects.requireNonNull(Path.of(path).toFile().listFiles()))
                .toList();
    }
}
