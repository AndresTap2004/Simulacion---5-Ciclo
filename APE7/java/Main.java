import controlador.MonteCarloController;
import vista.MonteCarloView;

import java.nio.file.Files;
import java.nio.file.Path;
import java.io.IOException;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) throws IOException {
        Path raizProyecto = encontrarRaizProyecto();
        MonteCarloController controlador = new MonteCarloController();
        MonteCarloController.ResultadoSimulacion[] resultados = controlador.procesarSimulaciones();
        MonteCarloView vista = new MonteCarloView();
        vista.mostrarResultados(resultados);
        Path archivoCsv = raizProyecto.resolve(Paths.get("java", "output", "resultados_java.csv"));
        Path directorioImg = raizProyecto.resolve("img");
        vista.guardarResultadosCsv(resultados, archivoCsv);
        System.out.println("Datos Java guardados en " + archivoCsv);
        System.out.println("Gráfica Java guardada en " +
                vista.generarGraficaConvergencia(resultados, directorioImg));
    }

    private static Path encontrarRaizProyecto() {
        Path directorio = Paths.get("").toAbsolutePath();
        while (directorio != null) {
            if (Files.isDirectory(directorio.resolve("java"))
                    && Files.isDirectory(directorio.resolve("python"))) {
                return directorio;
            }
            directorio = directorio.getParent();
        }
        throw new IllegalStateException("Ejecuta Main desde el proyecto APE7 o una de sus carpetas.");
    }
}