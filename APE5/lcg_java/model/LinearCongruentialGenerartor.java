package com.lcg.model;

public class LinearCongruentialGenerator {
    private long current;
    private final long a;
    private final long c;
    private final long m;
    private final long initialSeed;

    public LinearCongruentialGenerator(long seed, long a, long c, long m) {
        this.initialSeed = seed;
        this.current = seed;
        this.a = a;
        this.c = c;
        this.m = m;
    }

    public double nextValue() {
        // Usamos operaciones 'long' para evitar desbordamientos de enteros con 2^32
        current = (a * current + c) % m;
        return (double) current / m;
    }

    public double[] generateSequence(int n) {
        double[] sequence = new double[n];
        for (int i = 0; i < n; i++) {
            sequence[i] = nextValue();
        }
        return sequence;
    }

    public void reset() {
        this.current = this.initialSeed;
    }
}