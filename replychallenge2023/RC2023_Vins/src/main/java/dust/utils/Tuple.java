package dust.utils;

import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@EqualsAndHashCode
@RequiredArgsConstructor
public class Tuple<T1, T2> {
    private final T1 _1;
    private final T2 _2;
}
