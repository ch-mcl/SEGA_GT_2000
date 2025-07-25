
namespace SegaGT_ArchiveTool
{
    partial class Form1
    {
        /// <summary>
        /// 必要なデザイナー変数です。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 使用中のリソースをすべてクリーンアップします。
        /// </summary>
        /// <param name="disposing">マネージド リソースを破棄する場合は true を指定し、その他の場合は false を指定します。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows フォーム デザイナーで生成されたコード

        /// <summary>
        /// デザイナー サポートに必要なメソッドです。このメソッドの内容を
        /// コード エディターで変更しないでください。
        /// </summary>
        private void InitializeComponent()
        {
            this.progressBar1 = new System.Windows.Forms.ProgressBar();
            this.label_prog_text = new System.Windows.Forms.Label();
            this.label_prgoress_num = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.bgWorkerUnpack = new System.ComponentModel.BackgroundWorker();
            this.SuspendLayout();
            // 
            // progressBar1
            // 
            this.progressBar1.Location = new System.Drawing.Point(12, 24);
            this.progressBar1.Name = "progressBar1";
            this.progressBar1.Size = new System.Drawing.Size(301, 23);
            this.progressBar1.TabIndex = 0;
            // 
            // label_prog_text
            // 
            this.label_prog_text.AutoSize = true;
            this.label_prog_text.Location = new System.Drawing.Point(200, 56);
            this.label_prog_text.Name = "label_prog_text";
            this.label_prog_text.Size = new System.Drawing.Size(31, 12);
            this.label_prog_text.TabIndex = 1;
            this.label_prog_text.Text = "進捗:";
            // 
            // label_prgoress_num
            // 
            this.label_prgoress_num.AutoSize = true;
            this.label_prgoress_num.Location = new System.Drawing.Point(237, 56);
            this.label_prgoress_num.Name = "label_prgoress_num";
            this.label_prgoress_num.Size = new System.Drawing.Size(11, 12);
            this.label_prgoress_num.TabIndex = 2;
            this.label_prgoress_num.Text = "0";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(10, 9);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(231, 12);
            this.label3.TabIndex = 3;
            this.label3.Text = "Sega GT の.EXEをドラッグアンドドロップして起動";
            // 
            // bgWorkerUnpack
            // 
            this.bgWorkerUnpack.DoWork += new System.ComponentModel.DoWorkEventHandler(this.bgWorkerUnpack_DoWork);
            this.bgWorkerUnpack.ProgressChanged += new System.ComponentModel.ProgressChangedEventHandler(this.bgWorkerUnpack_ProgressChanged);
            this.bgWorkerUnpack.RunWorkerCompleted += new System.ComponentModel.RunWorkerCompletedEventHandler(this.bgWorkerUnpack_RunWorkerCompleted);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(325, 94);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label_prgoress_num);
            this.Controls.Add(this.label_prog_text);
            this.Controls.Add(this.progressBar1);
            this.Name = "Form1";
            this.Text = "Sega GT ArchiveTool";
            this.Shown += new System.EventHandler(this.Form1_Shown);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ProgressBar progressBar1;
        private System.Windows.Forms.Label label_prog_text;
        private System.Windows.Forms.Label label_prgoress_num;
        private System.Windows.Forms.Label label3;
        private System.ComponentModel.BackgroundWorker bgWorkerUnpack;
    }
}

