import controlador.MonteCarloController;
import vista.MonteCarloView;

import java.io.IOException;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) throws IOException {
        MonteCarloController controlador = new MonteCarloController();
        MonteCarloController.ResultadoSimulacion[] resultados = controlador.procesarSimulaciones();

        System.out.println("==========================================================================");
        System.out.println(" N          | Pi Estimado      | Error Absoluto   | Tiempo Java (ms)     ");
        System.out.println("==========================================================================");
        for (MonteCarloController.ResultadoSimulacion resultado : resultados) {
            System.out.printf("%-11d | %-16.6f | %-16.6f | %-20d%n",
                    resultado.getN(),
                    resultado.getPiEstimado(),
                    resultado.getErrorAbsoluto(),
                    resultado.getTiempoMs());
        }
        System.out.println("==========================================================================");

        MonteCarloView vista = new MonteCarloView();
        vista.guardarResultadosCsv(resultados, Paths.get("output", "resultados_java.csv"));
        System.out.println("Datos Java guardados en output\\resultados_java.csv");
        System.out.println("Gráfica Java guardada en " +
                vista.generarGraficaConvergencia(resultados, Paths.get("..", "img")));
    }
}