/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package lab5;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Scanner;

/**
 *
 * @author Jebu
 */
public class Graph {

    private ArrayList<LinkedList<Integer>> graph = new ArrayList<LinkedList<Integer>>();
    private int nodes;
     boolean reach = false;

    public void readGraph(File file) {
        
        System.out.println(reach);
        try {
            Scanner sc = new Scanner(file);
            int count = 0;
            while (sc.hasNextLine()) {

                this.graph.add(new LinkedList<Integer>());
                String i = sc.nextLine();
                String[] parts = i.split(" ");
                for (int a = 0; a < parts.length; a++) {
                    this.graph.get(count).add(Integer.parseInt(parts[a]));
                }
                count = count + 1;
            }
            sc.close();
            for (int c = 0; c < count; c++) {
                Collections.reverse(this.graph.get(c));
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }

    public void printGraph() {

        for (LinkedList<Integer> a : this.graph) {
            LinkedList<Integer> tempList = new LinkedList<Integer>();
            for (int c = 0; c < a.size() - 1; c++) {
                tempList.add(a.get(c));
            }
            System.out.println(a.get(a.size() - 1).toString() + ": " + tempList.toString());
        }
    }

    public int nodes() {
        
        this.nodes = this.graph.size();
        return this.nodes;
    }

    void dfs(int start, boolean visited[], int pred[], int searched) {
         if (start == searched) {
                this.reach= true;
                return;
            }
        
        searched = searched;
        visited[start] = true;
        for (Integer e : this.graph.get(start)) {
            if (e != null && visited[e] == false) {
                pred[e] = start;
                dfs(e, visited, pred, searched);
            }
        }

    }
}
