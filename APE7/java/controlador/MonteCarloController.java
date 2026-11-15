package controlador;

import modelo.MonteCarloModel;

public class MonteCarloController {
    private final int[] tamaniosMuestra = {1000, 10000, 100000, 1000000};

    public ResultadoSimulacion[] procesarSimulaciones() {
        ResultadoSimulacion[] resultados = new ResultadoSimulacion[tamaniosMuestra.length];

        for (int i = 0; i < tamaniosMuestra.length; i++) {
            int n = tamaniosMuestra[i];
            MonteCarloModel modelo = new MonteCarloModel();
            modelo.ejecutarSimulacion(n);

            resultados[i] = new ResultadoSimulacion(
                    modelo.getN(),
                    modelo.getPiEstimado(),
                    modelo.getErrorAbsoluto(),
                    modelo.getTiempoEjecucionMs()
            );
        }
        return resultados;
    }

    // Clase auxiliar interna para empaquetar los datos sin mezclar lógica de impresión
    public static class ResultadoSimulacion {
        private final int n;
        private final double piEstimado;
        private final double errorAbsoluto;
        private final long tiempoMs;

        public ResultadoSimulacion(int n, double piEstimado, double errorAbsoluto, long tiempoMs) {
            this.n = n;
            this.piEstimado = piEstimado;
            this.errorAbsoluto = errorAbsoluto;
            this.tiempoMs = tiempoMs;
        }

        public int getN() { return n; }
        public double getPiEstimado() { return piEstimado; }
        public double getErrorAbsoluto() { return errorAbsoluto; }
        public long getTiempoMs() { return tiempoMs; }
    }
}