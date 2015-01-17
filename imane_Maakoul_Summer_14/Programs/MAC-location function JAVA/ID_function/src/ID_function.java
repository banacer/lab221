import java.math.BigInteger;



public class ID_function {
	public static String mote_id;
    public static String room_id;
    public static String building_id;
    public static StringBuilder ID= new StringBuilder();
    //private static final byte[] mac_address = new byte[]{};
    
	public static void getLocation(String ID) {
               int length = ID.length();
	           if(length == 8){
	           mote_id=ID.substring(7);
	           room_id=ID.substring(3,7);
	           building_id=ID.substring(0,3);
	           System.out.println("mote number : " + mote_id );
	           System.out.println("room number : " + room_id );
	           System.out.println("building number : " + building_id );
	           
	           }
	}
	
	public static void getIdOf(int building, String room, int mote) {       
        ID.append(building).append(room).append(mote);   
        System.out.println("Mac @ is " + ID); 
        System.out.println(ID.toString());
        byte[] b = ID.toString().getBytes();
       
        System.out.println(b);
        System.out.println(b.length);
        
        //the address is 64bits
        System.out.println(String.format("%x", new BigInteger(1, ID.toString().getBytes(/*YOUR_CHARSET?*/))));
	}
	
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub

		getLocation("999999F9");
		System.out.println("\n");
		//Building n 111, room 210L, mote 2
		getIdOf(999,"999F", 9);
	}

}
