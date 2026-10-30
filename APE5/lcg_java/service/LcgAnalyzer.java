package com.lcg.service;

public class LcgAnalyzer {

    public static void printComparison(double[] seq1, double[] seq2, int limit) {
        System.out.printf("%-8s | %-15s | %-15s%n", "Índice", "Python (U_n)", "Java (U_n)");
        System.out.println("--------------------------------------------");
        int bound = Math.min(limit, Math.min(seq1.length, seq2.length));
        for (int i = 0; i < bound; i++) {
            System.out.printf("%-8d | %-15.6f | %-15.6f%n", (i + 1), seq1[i], seq2[i]);
        }
    }
}