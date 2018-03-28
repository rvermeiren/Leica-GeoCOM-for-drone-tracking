// compile .cs to .dll with VS15 console --> csc /r:IronPython.dll,Microsoft.Scripting.dll wrapper.cs
// compile .cs to .dll with VS15 console --> csc /t:library /r:IronPython.dll,Microsoft.Scripting.dll /out:leica_wrapper.dll wrapper.cs

using System;
using System.Threading;

using IronPython.Hosting;
using Microsoft.Scripting.Hosting;

namespace Wrapper
{
    public class Coord : EventArgs
    {
        public double x {get;set;}
        public double y {get;set;}
        public double z {get;set;}
        public int status{get;set;}
        public string toString(){
            return this.status +"("+this.x+","+this.y+","+this.z+")" ;
        }
    }

    public class Wrapper
    {
        public event EventHandler<Coord> ReceiveCoord;

        Thread thread;
        bool isContinue;
        ScriptRuntime ipy;
        dynamic test;

        public Wrapper()
        {}

        public void Open()
        {
            ipy = Python.CreateRuntime();
            test = ipy.UseFile("src/leica_track.py");
            test.open();

            isContinue = true;
            thread = new Thread(Run);
            thread.IsBackground = true;
            thread.Start();
        }

        public void Close()
        {
            isContinue = false;
        }

        public void  Run()
        {
            while(isContinue)
            {
                // Receive coord
                string rcv = (test.get_measure()).Replace('.',',');
                Console.WriteLine(rcv);
                String [] sxyz = rcv.Split(';');
                Coord c= new Coord();    // Parser coord
                c.status = int.Parse(sxyz[0]);
                if (c.status == 0)
                {
                    c.x = double.Parse(sxyz[1]);
                    c.y = double.Parse(sxyz[2]);
                    c.z = double.Parse(sxyz[3]);

                    ReceiveCoord?.Invoke(this, c);
                }  
            }
            test.close();
        }

        // static void eReceiveCoord(object sender, Coord c)
        // {
        //     Console.WriteLine(c.toString());
        // }
        //
        // static void Main()
        // {
        //     Wrapper w = new Wrapper();
        //     w.Open();
        //     w.ReceiveCoord += eReceiveCoord;
        //     while(true)
        //     {
        //         System.Threading.Thread.Sleep(100);
        //     }
        //     w.Close();
        // }
    }
}
