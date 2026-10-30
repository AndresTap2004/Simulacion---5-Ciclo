package com.lcg;

import com.lcg.model.LinearCongruentialGenerator;
import com.lcg.service.LcgAnalyzer;

public class Main {
    public static void main(String[] args) {
        long a = 1664525L;
        long c = 1013904223L;
        long m = 4294967296L; // 2^32
        long seed = 12345L;

        System.out.println("--- INICIALIZANDO GENERADOR LCG EN JAVA ---");
        LinearCongruentialGenerator lcgJava = new LinearCongruentialGenerator(seed, a, c, m);

        double[] valoresJava = lcgJava.generateSequence(10000);
        System.out.println("Se han generado " + valoresJava.length + " valores en Java.");

        // Simulando la secuencia de Python para efectos de comparación en consola
        LinearCongruentialGenerator lcgPythonSim = new LinearCongruentialGenerator(seed, a, c, m);
        double[] valoresPython = lcgPythonSim.generateSequence(10000);

        System.out.println("\n--- COMPARACIÓN DE LAS PRIMERAS 20 OBSERVACIONES ---");
        LcgAnalyzer.printComparison(valoresPython, valoresJava, 20);
    }
}