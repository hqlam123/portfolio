/**
 * State Capitals Quiz
 *
 * This program quizzes the user on U.S. state capitals.
 * It stores the states and capitals in a Map using HashMap,
 * displays the contents of the map,
 * and uses the TreeMap class to sort the map while using a binary search tree for storage.
 * The program prompts the user to enter a state and then displays the state's capital.
 *
 * Author: Huy Lam
 */

//import all util libraries for hash and treemap classes
import java.util.*;

public class stateCapitalsQuizMap {
    public static void main(String[] args) {
        //create HashMap for states and capitals with String as both key and value data type
        Map<String, String> stateCapitals = new HashMap<>();
        //insert key-value pairs in state-capital format
        stateCapitals.put("Alabama", "Montgomery");
        stateCapitals.put("Alaska", "Juneau");
        stateCapitals.put("Arizona", "Phoenix");
        stateCapitals.put("Arkansas", "Little Rock");
        stateCapitals.put("California", "Sacramento");
        stateCapitals.put("Colorado", "Denver");
        stateCapitals.put("Connecticut", "Hartford");
        stateCapitals.put("Delaware", "Dover");
        stateCapitals.put("Florida", "Tallahassee");
        stateCapitals.put("Georgia", "Atlanta");
        stateCapitals.put("Hawaii", "Honolulu");
        stateCapitals.put("Idaho", "Boise");
        stateCapitals.put("Illinois", "Springfield");
        stateCapitals.put("Indiana", "Indianapolis");
        stateCapitals.put("Iowa", "Des Moines");
        stateCapitals.put("Kansas", "Topeka");
        stateCapitals.put("Kentucky", "Frankfort");
        stateCapitals.put("Louisiana", "Baton Rouge");
        stateCapitals.put("Maine", "Augusta");
        stateCapitals.put("Maryland", "Annapolis");
        stateCapitals.put("Massachusetts", "Boston");
        stateCapitals.put("Michigan", "Lansing");
        stateCapitals.put("Minnesota", "St. Paul");
        stateCapitals.put("Mississippi", "Jackson");
        stateCapitals.put("Missouri", "Jefferson City");
        stateCapitals.put("Montana", "Helena");
        stateCapitals.put("Nebraska", "Lincoln");
        stateCapitals.put("Nevada", "Carson City");
        stateCapitals.put("New Hampshire", "Concord");
        stateCapitals.put("New Jersey", "Trenton");
        stateCapitals.put("New Mexico", "Santa Fe");
        stateCapitals.put("New York", "Albany");
        stateCapitals.put("North Carolina", "Raleigh");
        stateCapitals.put("North Dakota", "Bismarck");
        stateCapitals.put("Ohio", "Columbus");
        stateCapitals.put("Oklahoma", "Oklahoma City");
        stateCapitals.put("Oregon", "Salem");
        stateCapitals.put("Pennsylvania", "Harrisburg");
        stateCapitals.put("Rhode Island", "Providence");
        stateCapitals.put("South Carolina", "Columbia");
        stateCapitals.put("South Dakota", "Pierre");
        stateCapitals.put("Tennessee", "Nashville");
        stateCapitals.put("Texas", "Austin");
        stateCapitals.put("Utah", "Salt Lake City");
        stateCapitals.put("Vermont", "Montpelier");
        stateCapitals.put("Virginia", "Richmond");
        stateCapitals.put("Washington", "Olympia");
        stateCapitals.put("West Virginia", "Charleston");
        stateCapitals.put("Wisconsin", "Madison");
        stateCapitals.put("Wyoming", "Cheyenne");

        //print the HashMap
        System.out.println("State and capitals:");
        //iterate over each entry in the Map
        for (Map.Entry<String, String> entry : stateCapitals.entrySet()) {
            //print the Map via Key and Value
            System.out.println(entry.getKey() + " - " + entry.getValue());
        }
        System.out.println();

        //create TreeMap to sort the map
        Map<String, String> sortedCapitals = new TreeMap<>(stateCapitals);

        //initialize scanner to accept user input
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter a state: ");
        //store input in userState
        String userState = scanner.nextLine();

        //print capital for state input
        String capital = sortedCapitals.get(userState);
        //check if capital exists
        if (capital != null) {
            System.out.println("The capital of " + userState + " is " + capital + ".");
        } else {
            System.out.println(userState + " is not a state.");
        }

        scanner.close();
    }
}