using SegaGT_ArchiveTool.Models;
using SegaGT_ArchiveTool.SEGAGTLib;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace SegaGT_ArchiveTool
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Shown(object sender, EventArgs e)
        {
            if (bgWorkerUnpack.IsBusy)
            {
                return;
            }

            string[] paths = Environment.GetCommandLineArgs();
            // not set files
            if (paths.Count() == 1)
            {
                return;
            } else if(paths.Count() > 2)
            {
                return;
            } else if (Path.GetExtension(paths[1]).ToLower() != ".exe")
            {
                return;
            }

            progressBar1.Minimum = 0;
            progressBar1.Value = 0;

            string region = "EMPIRE";

            // Get Values from Master Table
            TOC_Table tocTabl = new TOC_Table();
            DataRow[] dataRows = tocTabl.tocTable.Select($"region = '{region}'");
            DataRow row = dataRows[0];

            ArgsDoWorker argsDoWoker = new ArgsDoWorker();

            argsDoWoker.filePath = paths[1];
            argsDoWoker.fileDirectory = Path.GetDirectoryName(paths[1]);


            List<TOC_Entry> entrys = new List<TOC_Entry>();
            TOC_Entry str0 = (TOC_Entry)row[TOC_Table.COL_NAME_STR0];
            entrys.Add(str0);
            TOC_Entry str1 = (TOC_Entry)row[TOC_Table.COL_NAME_STR1];
            entrys.Add(str1);
            TOC_Entry str2 = (TOC_Entry)row[TOC_Table.COL_NAME_STR2];
            entrys.Add(str2);
            TOC_Entry str3 = (TOC_Entry)row[TOC_Table.COL_NAME_STR3];
            entrys.Add(str3);
            argsDoWoker.entrys = entrys;

            int totalFileCount = str0.count + str1.count + str2.count + str3.count;
            argsDoWoker.totalFileCount = totalFileCount;
            progressBar1.Maximum = totalFileCount;

            // Unpack
            bgWorkerUnpack.WorkerReportsProgress = true;
            bgWorkerUnpack.RunWorkerAsync(argsDoWoker);

        }

        // Unpack
        private void bgWorkerUnpack_DoWork(object sender, DoWorkEventArgs e)
        {
            BackgroundWorker bgWorker = (BackgroundWorker)sender;
            ArgsDoWorker argments = e.Argument as ArgsDoWorker;
            string filePath = argments.filePath; // path of tbl file
            string fileDirectory = argments.fileDirectory;

            List<TOC_Entry> entrys = argments.entrys;

            int totalFileCount = entrys[0].count + entrys[1].count + entrys[2].count + entrys[3].count;

            UserStateProgressChanged argsProgressChanged = new UserStateProgressChanged();
            argsProgressChanged.maximum = totalFileCount;
            int progress = 0;

            try
            {
                progress = Unpack(0, bgWorker, filePath, fileDirectory, entrys, argsProgressChanged, progress);
                progress = Unpack(1, bgWorker, filePath, fileDirectory, entrys, argsProgressChanged, progress);
                progress = Unpack(2, bgWorker, filePath, fileDirectory, entrys, argsProgressChanged, progress);
                progress = Unpack(3, bgWorker, filePath, fileDirectory, entrys, argsProgressChanged, progress);

            }
            catch
            {
                bgWorker.ReportProgress(progress, argsProgressChanged);
                return;
            }

            MessageBox.Show("Success: Unpack Complete.");



        }

        private static int Unpack(int idx, BackgroundWorker bgWorker, string filePath, string fileDirectory, List<TOC_Entry> entrys, UserStateProgressChanged argsProgressChanged, int progress)
        {
            // EXE file of SsegGT
            using (FileStream exeFileStream = new FileStream(filePath, FileMode.Open, FileAccess.Read))
            {
                // STRn(n=0~3) file
                string targetArcName = $"STR{idx}";
                string destDirectoryPath = $@"{fileDirectory}\extract\{targetArcName}";
                Directory.CreateDirectory(destDirectoryPath);
                int fileCount = entrys[idx].count;
                exeFileStream.Seek(entrys[idx].adr, SeekOrigin.Begin);
                using (FileStream arcFileStream = new FileStream($@"{fileDirectory}\{targetArcName}.BIN", FileMode.Open, FileAccess.Read))
                {
                    for (int i = 0; i < fileCount; i++)
                    {
                        Entry entry = new Entry();
                        entry.Unpack(exeFileStream);
                        if (i > 0 && entry.offset < 1)
                        {
                            exeFileStream.Seek(-8, SeekOrigin.Current);
                            break;
                        }

                        byte[] destBytes = new byte[entry.size];
                        arcFileStream.Seek(entry.offset, SeekOrigin.Begin);
                        arcFileStream.Read(destBytes, 0x00, entry.size);

                        string extension = "bin";
                        if (destBytes.Length > 2 && destBytes[0] == 0x4E && destBytes[1] == 0x4A)
                        {
                            // NJ file
                            extension = "nj";
                        } else if (destBytes.Length > 4 && destBytes[0] == 0x47 && destBytes[1] == 0x42 && destBytes[2] == 0x49 && destBytes[3] == 0x58){
                            extension = "pvr";
                        }

                        string destFileName = string.Format("{0:D8}.{1}", i, extension);
                        string fullpath = $@"{destDirectoryPath}\{destFileName}";
                        using (FileStream destFileStream = new FileStream(fullpath, FileMode.Create, FileAccess.Write))
                        {
                            destFileStream.Write(destBytes, 0x00, entry.size);
                        }

                        progress++;
                        bgWorker.ReportProgress(progress, argsProgressChanged); // update progress var
                    }

                }

            }

            return progress;
        }

        // Unpackに関する表示の更新。
        private void bgWorkerUnpack_ProgressChanged(object sender, ProgressChangedEventArgs e)
        {
            //UserStateProgressChanged userState = e.UserState as UserStateProgressChanged;
            //progressBar1.Maximum = userState.maximum;

            progressBar1.Value = e.ProgressPercentage;
            label_prgoress_num.Text = $@"{e.ProgressPercentage.ToString()}/{ progressBar1.Maximum.ToString()}";

        }

        private void bgWorkerUnpack_RunWorkerCompleted(object sender, RunWorkerCompletedEventArgs e)
        {

        }
    }

}
