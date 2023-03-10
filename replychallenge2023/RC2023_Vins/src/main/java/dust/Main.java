package dust;

import dust.utils.IOHelper;
import lombok.extern.slf4j.Slf4j;

import java.io.File;

@Slf4j
public class Main {
    public static void main(String[] args) {
        String inPath = "data/in";
        String outPath = "data/out";

        for (var file : IOHelper.getFilesInDirectory(inPath)) {
            log.info("Processing file {}...", file.getName());

            log.trace("Reading input from {}...", file.getName());
            var content = IOHelper.read(file);

            log.trace("Parsing input from {}...", file.getName());
            var inputParser = new InputParser();
            inputParser.parseInput(content);

            log.trace("Starting execution for file {}...", file.getName());
            var engine = new Engine(inputParser.getNetwork(), inputParser.getSnakes());
            engine.start();

            log.trace("Serializing output for file {}...", file.getName());
            var outputSerializer = new OutputSerializer();
            var output = outputSerializer.serializeOutput(inputParser.getSnakes());

            log.trace("Writing output for file {}...", file.getName());
            IOHelper.write(new File(outPath, file.getName()), output);

            log.info("Processed file: {}.", file.getName());
        }
    }
}
