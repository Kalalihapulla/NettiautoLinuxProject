/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package lab5;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;

/**
 *
 * @author Jebu
 */
public class Lab5 {

    /* find a maze solution */
    private static int mazeSolution(int from, int to, int pred[], int steps[]) {

        int i, n, node;

        // first count how many edges between the end and the start
        node = to;
        n = 1;

        while ((node = pred[node]) != from) {

            n++;

        }

        // then reverse pred[] array to steps[] array
        node = to;
        i = n;

        while (i >= 0) {
            steps[i--] = node;
            node = pred[node];
        }

        // include also the end vertex
        return (n + 1);
    }

    private final static String FILE = "C:/Users/Jebu/Desktop/lab5/maze.grh";
    private final static String FILE2 = "C:/Users/Jebu/Desktop/lab5/maze2.grh";
    private final static String FILE3 = "C:/Users/Jebu/Desktop/lab5/maze3.grh";
    private final static String FILE4 = "C:/Users/Jebu/Desktop/lab5/maze4.grh";

    static String[] mazeArray = {FILE, FILE2, FILE3, FILE4};

    private final static int FROM = 0;
    private final static int TO = 15;

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws IOException {
        
        int count = 4;
        try {
            String arg1 = args[0];

            count = Integer.parseInt(arg1);
            if (count > 4) {
                count = 4;

                System.out.println("Max is 4");
            }
        } catch (Exception e) {
        }
        
        String FILENAME = "output.txt";
        
       	BufferedWriter bw = null;
	FileWriter fw = null;
 
	fw = new FileWriter(FILENAME);
        bw = new BufferedWriter(fw);

        String solution;
       
        for (int i = 0; i < count; i++) {
            Graph g = new Graph();

            // read the graph. and do the depth-first search
            System.out.println("Graph Adjacent list");
            g.readGraph(new File(mazeArray[i]));
            g.printGraph();

            boolean visited[] = new boolean[g.nodes()];
            int pred[] = new int[g.nodes()];
            g.dfs(FROM, visited, pred, g.nodes() - 1);

            System.out.println("Pred array: " + Arrays.toString(pred));
            System.out.println("Visited array: " + Arrays.toString(visited).replace("true", "1").replace("false", "0"));

            // then check if there is a solution by looking from the backwards to the start
            int steps[] = new int[g.nodes()];

            System.out.println("\nMaze solution from " + FROM + " to " + TO);

            int n = mazeSolution(FROM, TO, pred, steps);

           if (g.reach) {

                for (int u = 0; u < n; u++) {       
                   
                    solution = steps[u] + " ";
                    
                    bw.write(solution);
                                    
                }

            } else {
                solution = "No solution for given maze";
  
                bw.write(solution);
            }
            bw.write(System.getProperty("line.separator"));
           
        }
        
        
        bw.close();
        fw.close();
    }

}
