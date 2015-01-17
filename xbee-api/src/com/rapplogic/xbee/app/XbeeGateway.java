/**
 * Copyright (c) 2008 Andrew Rapp. All rights reserved.
 *  
 * This file is part of XBee-API.
 *  
 * XBee-API is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *  
 * XBee-API is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *  
 * You should have received a copy of the GNU General Public License
 * along with XBee-API.  If not, see <http://www.gnu.org/licenses/>.
 */

package com.rapplogic.xbee.app;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.URL;
import java.net.URLConnection;

import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;

import com.rapplogic.xbee.api.PacketParser;
import com.rapplogic.xbee.api.XBee;
import com.rapplogic.xbee.api.XBeeException;
import com.rapplogic.xbee.api.XBeeResponse;
import com.rapplogic.xbee.api.wpan.RxResponse16;
import com.rapplogic.xbee.api.zigbee.ZNetRxResponse;
import com.rapplogic.xbee.util.ByteUtils;

/** 
 * @author andrew
 */
public class XbeeGateway {

	//private final static Logger log = Logger.getLogger(XbeeGateway.class);
	
	private XbeeGateway(String device) throws XBeeException, IOException {
		
		XBee xbee = new XBee();		
		try 
		{
			
			xbee.open(device, 9600);
			
			while (true) 
			{				
				XBeeResponse response = xbee.getResponse();
				RxResponse16 rx = (RxResponse16) response;
				String token = rx.getSourceAddress().toString();
				String nodeId = ""+token.charAt(2)+token.charAt(3)+token.charAt(7)+'_'+token.charAt(8);
				//System.out.println("source address: "+nodeId);
				//DO MAPPING BETWEEN ADDRESS AND NODE ID
				
				int[] bytes = response.getProcessedPacketBytes();
				
				int merged = ((bytes[8] & 0xff) << 8 ) | ((bytes[9] & 0xff) & 0xff);
				//int merged2 = ((bytes[13] & 0xff) << 8 ) | ((bytes[14] & 0xff) & 0xff);
				//int merged =  ((((bytes[11] & 0xff) << 8 ) | ((bytes[12] & 0xff) & 0xff) & 0xff) << 8 ) | 
				//		((((bytes[13] & 0xff) << 8 ) | ((bytes[14] & 0xff) & 0xff) & 0xff) & 0xff);
				double data = 0;
				data = merged;
				
				if((int)bytes[7] == 1 || (int)bytes[7] == 2)
					data = ((double) merged) / 100;
				
				else if ((int)bytes[7] == 0)
					data = ((double) merged) / 10;				
				
				
				URL url = null;
				BufferedWriter bw = null;
				switch((int)bytes[7])
				{
				case 0:
					url = new URL("http://localhost:8080/httpds?"+nodeId+"C="+data);
					//System.out.println("co2 = "+(double) merged/10);
					
					break;
				case 1:
					url = new URL("http://localhost:8080/httpds?"+nodeId+"H="+data);
					//System.out.println("hum = "+(double)merged/100);
					
					break;
				case 2:
					data = (9/5)*(data + 32); // convert from C to F
					url = new URL("http://localhost:8080/httpds?"+nodeId+"T="+data);
					//System.out.println("temp = "+(double) data);
					break;
				case 3:
					url = new URL("http://localhost:8080/httpds?"+nodeId+"UL="+data);
					//System.out.println("UL = "+(double) data);
					break;
				case 4:
					url = new URL("http://localhost:8080/httpds?"+nodeId+"UR="+data);
					//System.out.println("UR = "+(double) data);
					break;
				case 5:
					url = new URL("http://localhost:8080/httpds?"+nodeId+"UT="+data);
					//System.out.println("UT = "+(double) data);					
					break;	
					
				}
				
				URLConnection myURLConnection = url.openConnection();
			    myURLConnection.connect();
			    System.out.println(url.toString());
				Thread.sleep(500);
				
			}
			
		}
		catch(Exception ex)
		{
			ex.printStackTrace();
		}
		finally 
		{
			if (xbee != null && xbee.isConnected())
			{
				xbee.close();		
			}
		}
	}
	
	public static void main(String[] args) throws XBeeException, InterruptedException, IOException  
	{
		//PropertyConfigurator.configure("log4j.properties");
		new XbeeGateway(args[0]);
	}
}
