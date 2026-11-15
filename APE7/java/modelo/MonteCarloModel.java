package modelo;

import java.util.Random;

public class MonteCarloModel {
    private int n;
    private double piEstimado;
    private double errorAbsoluto;
    private long tiempoEjecucionMs;

    public void ejecutarSimulacion(int n) {
        this.n = n;
        Random random = new Random();
        int puntosDentro = 0;

        long inicio = System.nanoTime();
        for (int i = 0; i < n; i++) {
            double x = random.nextDouble();
            double y = random.nextDouble();
            if (x * x + y * y <= 1.0) {
                puntosDentro++;
            }
        }
        long fin = System.nanoTime();

        this.piEstimado = 4.0 * puntosDentro / n;
        this.errorAbsoluto = Math.abs(Math.PI - this.piEstimado);
        this.tiempoEjecucionMs = (fin - inicio) / 1_000_000;
    }

    public int getN() { return n; }
    public double getPiEstimado() { return piEstimado; }
    public double getErrorAbsoluto() { return errorAbsoluto; }
    public long getTiempoEjecucionMs() { return tiempoEjecucionMs; }
}