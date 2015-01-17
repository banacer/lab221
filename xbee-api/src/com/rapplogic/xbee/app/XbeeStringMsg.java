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

import java.io.IOException;
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
public class XbeeStringMsg {

	//private final static Logger log = Logger.getLogger(XbeeGateway.class);
	
	private XbeeStringMsg(String device) throws XBeeException, IOException {
		
		XBee xbee = new XBee();		
		try 
		{
			
			xbee.open(device, 9600);
			
			while (true) 
			{				
				XBeeResponse response = xbee.getResponse();
				RxResponse16 rx = (RxResponse16) response;
				System.out.println("source address is: "+rx.getSourceAddress().toString());
				int[] data = response.getProcessedPacketBytes();
				String msg = "";
				for(int i =7; i < data.length - 1; i++)
				{					
					msg+= (char) data[i];					
				}
				System.out.println(msg);
			}
			
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
		new XbeeStringMsg(args[0]);
	}
}
