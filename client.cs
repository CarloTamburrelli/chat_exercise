using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
 
class Program
{
    static void getMessages(object ns)
    {
        NetworkStream obj = (NetworkStream)ns;
        int sizeData = 1024;
        byte[] receivedBytes = new byte[sizeData];
        int byte_count;
        try
        {
            while ((byte_count = obj.Read(receivedBytes, 0, receivedBytes.Length)) > 0)
            {
                byte[] formated = new byte[byte_count];
                //handle  the null characteres in the byte array
                Array.Copy(receivedBytes, formated, byte_count);
                string data = Encoding.ASCII.GetString(formated);
                if (data == "---") {
                    System.Environment.Exit(1);
                }
                Console.WriteLine(data);
            }
        }
        catch (Exception e)
        {
            Console.WriteLine("Error reading buffer.");
        }
    }
 
    static void Main(string[] args)
    {   
        Console.WriteLine("Establecer a dirección IP");
        string address = Console.ReadLine();
        Console.WriteLine("Establecer una puerta");
        string port = Console.ReadLine();
        IPAddress ip = IPAddress.Parse(address);
        TcpClient client = new TcpClient();
        try {
            client.Connect(ip, Int32.Parse(port));
            NetworkStream ns = client.GetStream();
            Console.WriteLine("conectado al servidor "+address+":"+port);
            Console.WriteLine("Elige un nombre:");
            Thread task = new Thread(getMessages);
            task.Start(ns);
            string s;
            while (true)
            {
                s = Console.ReadLine();
                byte[] buffer = Encoding.ASCII.GetBytes(s);
                ns.Write(buffer, 0, buffer.Length);
            }
            ns.Close();
            client.Close();
            Console.WriteLine("disconnect from server.");
        }catch (SocketException e)
            {
                Console.WriteLine("No server found");
            }
    }
}