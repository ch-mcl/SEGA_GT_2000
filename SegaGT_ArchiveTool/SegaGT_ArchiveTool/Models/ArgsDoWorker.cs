using SegaGT_ArchiveTool.SEGAGTLib;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SegaGT_ArchiveTool.Models
{
    class ArgsDoWorker
    {
        public string filePath;
        public string fileDirectory;
        public int totalFileCount;
        public List<TOC_Entry> entrys = new List<TOC_Entry>();

    }
}
