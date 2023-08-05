from __future__ import absolute_import
from __future__ import print_function
import veriloggen
import axi_vecadd

expected_verilog = """
module test;

  reg CLK;
  reg RST;
  reg [32-1:0] slave_awaddr;
  reg [8-1:0] slave_awlen;
  reg slave_awvalid;
  wire slave_awready;
  reg [32-1:0] slave_wdata;
  reg [4-1:0] slave_wstrb;
  reg slave_wlast;
  reg slave_wvalid;
  wire slave_wready;
  reg [32-1:0] slave_araddr;
  reg [8-1:0] slave_arlen;
  reg slave_arvalid;
  wire slave_arready;
  wire [32-1:0] slave_rdata;
  wire slave_rlast;
  wire slave_rvalid;
  reg slave_rready;
  wire [32-1:0] master_awaddr;
  wire [8-1:0] master_awlen;
  wire master_awvalid;
  reg master_awready;
  wire [32-1:0] master_wdata;
  wire [4-1:0] master_wstrb;
  wire master_wlast;
  wire master_wvalid;
  reg master_wready;
  wire [32-1:0] master_araddr;
  wire [8-1:0] master_arlen;
  wire master_arvalid;
  reg master_arready;
  reg [32-1:0] master_rdata;
  reg master_rlast;
  reg master_rvalid;
  wire master_rready;
  reg [32-1:0] waddr;
  localparam waddr_init = 0;
  reg [32-1:0] _awlen;
  reg [32-1:0] raddr;
  localparam raddr_init = 0;
  reg [32-1:0] _arlen;
  reg [32-1:0] _d1_raddr;
  reg _raddr_cond_3_0_1;
  wire _tmp_0;
  assign _tmp_0 = 1;

  always @(*) begin
    slave_awvalid <= _tmp_0;
  end

  wire [32-1:0] _tmp_1;
  assign _tmp_1 = 256;

  always @(*) begin
    slave_awaddr <= _tmp_1;
  end

  wire [8-1:0] _tmp_2;
  assign _tmp_2 = 0;

  always @(*) begin
    slave_awlen <= _tmp_2;
  end

  wire _tmp_3;
  assign _tmp_3 = 1;

  always @(*) begin
    slave_arvalid <= _tmp_3;
  end

  wire [32-1:0] _tmp_4;
  assign _tmp_4 = 256;

  always @(*) begin
    slave_araddr <= _tmp_4;
  end

  wire [8-1:0] _tmp_5;
  assign _tmp_5 = 0;

  always @(*) begin
    slave_arlen <= _tmp_5;
  end

  wire _tmp_6;
  assign _tmp_6 = 1;

  always @(*) begin
    slave_wvalid <= _tmp_6;
  end

  wire [32-1:0] _tmp_7;
  assign _tmp_7 = 512;

  always @(*) begin
    slave_wdata <= _tmp_7;
  end

  wire [4-1:0] _tmp_8;
  assign _tmp_8 = { 4{ 1'd1 } };

  always @(*) begin
    slave_wstrb <= _tmp_8;
  end

  wire _tmp_9;
  assign _tmp_9 = 1;

  always @(*) begin
    slave_wlast <= _tmp_9;
  end

  wire _tmp_10;
  assign _tmp_10 = 1;

  always @(*) begin
    slave_rready <= _tmp_10;
  end


  main
  uut
  (
    .CLK(CLK),
    .RST(RST),
    .slave_awaddr(slave_awaddr),
    .slave_awlen(slave_awlen),
    .slave_awvalid(slave_awvalid),
    .slave_awready(slave_awready),
    .slave_wdata(slave_wdata),
    .slave_wstrb(slave_wstrb),
    .slave_wlast(slave_wlast),
    .slave_wvalid(slave_wvalid),
    .slave_wready(slave_wready),
    .slave_araddr(slave_araddr),
    .slave_arlen(slave_arlen),
    .slave_arvalid(slave_arvalid),
    .slave_arready(slave_arready),
    .slave_rdata(slave_rdata),
    .slave_rlast(slave_rlast),
    .slave_rvalid(slave_rvalid),
    .slave_rready(slave_rready),
    .master_awaddr(master_awaddr),
    .master_awlen(master_awlen),
    .master_awvalid(master_awvalid),
    .master_awready(master_awready),
    .master_wdata(master_wdata),
    .master_wstrb(master_wstrb),
    .master_wlast(master_wlast),
    .master_wvalid(master_wvalid),
    .master_wready(master_wready),
    .master_araddr(master_araddr),
    .master_arlen(master_arlen),
    .master_arvalid(master_arvalid),
    .master_arready(master_arready),
    .master_rdata(master_rdata),
    .master_rlast(master_rlast),
    .master_rvalid(master_rvalid),
    .master_rready(master_rready)
  );


  initial begin
    $dumpfile("uut.vcd");
    $dumpvars(0, uut, CLK, RST, slave_awaddr, slave_awlen, slave_awvalid, slave_awready, slave_wdata, slave_wstrb, slave_wlast, slave_wvalid, slave_wready, slave_araddr, slave_arlen, slave_arvalid, slave_arready, slave_rdata, slave_rlast, slave_rvalid, slave_rready, master_awaddr, master_awlen, master_awvalid, master_awready, master_wdata, master_wstrb, master_wlast, master_wvalid, master_wready, master_araddr, master_arlen, master_arvalid, master_arready, master_rdata, master_rlast, master_rvalid, master_rready, waddr, _awlen, raddr, _arlen, _d1_raddr, _raddr_cond_3_0_1, _tmp_0, _tmp_1, _tmp_2, _tmp_3, _tmp_4, _tmp_5, _tmp_6, _tmp_7, _tmp_8, _tmp_9, _tmp_10);
  end


  initial begin
    CLK = 0;
    forever begin
      #5 CLK = !CLK;
    end
  end


  initial begin
    RST = 0;
    waddr = waddr_init;
    _awlen = 0;
    raddr = raddr_init;
    _arlen = 0;
    _d1_raddr = raddr_init;
    _raddr_cond_3_0_1 = 0;
    #100;
    RST = 1;
    #100;
    RST = 0;
    #100000;
    $finish;
  end

  localparam waddr_1 = 1;
  localparam waddr_2 = 2;
  localparam waddr_3 = 3;
  localparam waddr_4 = 4;
  localparam waddr_5 = 5;
  localparam waddr_6 = 6;
  localparam waddr_7 = 7;
  localparam waddr_8 = 8;

  always @(posedge CLK) begin
    if(RST) begin
      waddr <= waddr_init;
      _awlen <= 0;
    end else begin
      case(waddr)
        waddr_init: begin
          master_awready <= 0;
          master_wready <= 0;
          _awlen <= 0;
          if(master_awvalid) begin
            waddr <= waddr_1;
          end 
        end
        waddr_1: begin
          if(master_awvalid) begin
            master_awready <= 1;
          end 
          waddr <= waddr_2;
        end
        waddr_2: begin
          master_awready <= 0;
          _awlen <= master_awlen;
          waddr <= waddr_3;
        end
        waddr_3: begin
          master_wready <= 0;
          if(master_wvalid) begin
            waddr <= waddr_4;
          end 
        end
        waddr_4: begin
          if(master_wvalid) begin
            master_wready <= 1;
          end 
          waddr <= waddr_5;
        end
        waddr_5: begin
          master_wready <= 0;
          waddr <= waddr_6;
        end
        waddr_6: begin
          waddr <= waddr_7;
        end
        waddr_7: begin
          waddr <= waddr_8;
        end
        waddr_8: begin
          _awlen <= _awlen - 1;
          waddr <= waddr_3;
          if(_awlen == 0) begin
            waddr <= waddr_init;
          end 
        end
      endcase
    end
  end

  localparam raddr_1 = 1;
  localparam raddr_2 = 2;
  localparam raddr_3 = 3;
  localparam raddr_4 = 4;
  localparam raddr_5 = 5;
  localparam raddr_6 = 6;
  localparam raddr_7 = 7;
  localparam raddr_8 = 8;
  localparam raddr_9 = 9;
  localparam raddr_10 = 10;

  always @(posedge CLK) begin
    if(RST) begin
      raddr <= raddr_init;
      _d1_raddr <= raddr_init;
      _arlen <= 0;
      _raddr_cond_3_0_1 <= 0;
    end else begin
      _d1_raddr <= raddr;
      case(_d1_raddr)
        raddr_3: begin
          if(_raddr_cond_3_0_1) begin
            master_rvalid <= 0;
            master_rlast <= 0;
          end 
        end
      endcase
      case(raddr)
        raddr_init: begin
          master_arready <= 0;
          master_rdata <= -1;
          master_rvalid <= 0;
          master_rlast <= 0;
          if(master_arvalid) begin
            raddr <= raddr_1;
          end 
        end
        raddr_1: begin
          if(master_arvalid) begin
            master_arready <= 1;
            master_rdata <= master_araddr - 1;
          end 
          raddr <= raddr_2;
        end
        raddr_2: begin
          master_arready <= 0;
          _arlen <= master_arlen;
          raddr <= raddr_3;
        end
        raddr_3: begin
          if((master_rready || !master_rvalid) && !master_rlast) begin
            master_rdata <= master_rdata + 1;
            master_rvalid <= 1;
            master_rlast <= 0;
            _arlen <= _arlen - 1;
          end 
          if((master_rready || !master_rvalid) && !master_rlast && (_arlen == 0)) begin
            master_rlast <= 1;
          end 
          _raddr_cond_3_0_1 <= 1;
          raddr <= raddr_4;
        end
        raddr_4: begin
          if(master_rvalid && !master_rready) begin
            master_rvalid <= master_rvalid;
            master_rlast <= master_rlast;
          end 
          if(master_rvalid && master_rready) begin
            raddr <= raddr_5;
          end 
        end
        raddr_5: begin
          raddr <= raddr_6;
        end
        raddr_6: begin
          raddr <= raddr_7;
        end
        raddr_7: begin
          raddr <= raddr_8;
        end
        raddr_8: begin
          if((_arlen + 1 & 255) != 0) begin
            raddr <= raddr_3;
          end 
          if((_arlen + 1 & 255) == 0) begin
            raddr <= raddr_9;
          end 
        end
        raddr_9: begin
          raddr <= raddr_10;
        end
        raddr_10: begin
          raddr <= raddr_init;
        end
      endcase
    end
  end


endmodule



module main
(
  input CLK,
  input RST,
  input [32-1:0] slave_awaddr,
  input [8-1:0] slave_awlen,
  input slave_awvalid,
  output slave_awready,
  input [32-1:0] slave_wdata,
  input [4-1:0] slave_wstrb,
  input slave_wlast,
  input slave_wvalid,
  output slave_wready,
  input [32-1:0] slave_araddr,
  input [8-1:0] slave_arlen,
  input slave_arvalid,
  output slave_arready,
  output reg [32-1:0] slave_rdata,
  output reg slave_rlast,
  output reg slave_rvalid,
  input slave_rready,
  output reg [32-1:0] master_awaddr,
  output reg [8-1:0] master_awlen,
  output reg master_awvalid,
  input master_awready,
  output reg [32-1:0] master_wdata,
  output reg [4-1:0] master_wstrb,
  output reg master_wlast,
  output reg master_wvalid,
  input master_wready,
  output reg [32-1:0] master_araddr,
  output reg [8-1:0] master_arlen,
  output reg master_arvalid,
  input master_arready,
  input [32-1:0] master_rdata,
  input master_rlast,
  input master_rvalid,
  output master_rready
);

  reg [10-1:0] ram_a_0_addr;
  wire [32-1:0] ram_a_0_rdata;
  reg [32-1:0] ram_a_0_wdata;
  reg ram_a_0_wenable;

  ram_a
  inst_ram_a
  (
    .CLK(CLK),
    .ram_a_0_addr(ram_a_0_addr),
    .ram_a_0_rdata(ram_a_0_rdata),
    .ram_a_0_wdata(ram_a_0_wdata),
    .ram_a_0_wenable(ram_a_0_wenable)
  );

  reg [10-1:0] ram_b_0_addr;
  wire [32-1:0] ram_b_0_rdata;
  reg [32-1:0] ram_b_0_wdata;
  reg ram_b_0_wenable;

  ram_b
  inst_ram_b
  (
    .CLK(CLK),
    .ram_b_0_addr(ram_b_0_addr),
    .ram_b_0_rdata(ram_b_0_rdata),
    .ram_b_0_wdata(ram_b_0_wdata),
    .ram_b_0_wenable(ram_b_0_wenable)
  );

  reg [10-1:0] ram_c_0_addr;
  wire [32-1:0] ram_c_0_rdata;
  reg [32-1:0] ram_c_0_wdata;
  reg ram_c_0_wenable;

  ram_c
  inst_ram_c
  (
    .CLK(CLK),
    .ram_c_0_addr(ram_c_0_addr),
    .ram_c_0_rdata(ram_c_0_rdata),
    .ram_c_0_wdata(ram_c_0_wdata),
    .ram_c_0_wenable(ram_c_0_wenable)
  );

  reg [32-1:0] fsm;
  localparam fsm_init = 0;
  reg [9-1:0] _tmp_0;
  reg [32-1:0] _tmp_1;
  reg _tmp_2;
  reg _tmp_3;
  assign slave_awready = (fsm == 0) && !_tmp_2 && _tmp_3;
  assign slave_wready = fsm == 1;
  reg [32-1:0] _tmp_fsm_0;
  localparam _tmp_fsm_0_init = 0;
  reg [9-1:0] _tmp_4;
  reg _master_cond_0_1;
  wire _tmp_5;
  wire _tmp_6;
  assign _tmp_6 = 1;
  reg [8-1:0] _tmp_7;
  reg _tmp_8;
  wire [32-1:0] _tmp_data_9;
  wire _tmp_valid_9;
  wire _tmp_ready_9;
  assign _tmp_ready_9 = (_tmp_7 > 0) && !_tmp_8;
  reg _ram_a_cond_0_1;
  reg [32-1:0] _tmp_fsm_1;
  localparam _tmp_fsm_1_init = 0;
  reg [9-1:0] _tmp_10;
  reg _master_cond_1_1;
  wire _tmp_11;
  wire _tmp_12;
  assign _tmp_12 = 1;
  assign master_rready = _tmp_5 && _tmp_6 || _tmp_11 && _tmp_12;
  reg [8-1:0] _tmp_13;
  reg _tmp_14;
  wire [32-1:0] _tmp_data_15;
  wire _tmp_valid_15;
  wire _tmp_ready_15;
  assign _tmp_ready_15 = (_tmp_13 > 0) && !_tmp_14;
  reg _ram_b_cond_0_1;
  reg _tmp_16;
  reg _tmp_17;
  wire _tmp_18;
  wire _tmp_19;
  assign _tmp_19 = 1;
  localparam _tmp_20 = 1;
  wire [_tmp_20-1:0] _tmp_21;
  assign _tmp_21 = (_tmp_18 || !_tmp_16) && (_tmp_19 || !_tmp_17);
  reg [_tmp_20-1:0] __tmp_21_1;
  wire [32-1:0] _tmp_22;
  reg [32-1:0] __tmp_22_1;
  assign _tmp_22 = (__tmp_21_1)? ram_a_0_rdata : __tmp_22_1;
  reg [8-1:0] _tmp_23;
  reg _tmp_24;
  reg _tmp_25;
  reg _tmp_26;
  reg _tmp_27;
  reg _tmp_28;
  reg _tmp_29;
  wire _tmp_30;
  wire _tmp_31;
  assign _tmp_31 = 1;
  localparam _tmp_32 = 1;
  wire [_tmp_32-1:0] _tmp_33;
  assign _tmp_33 = (_tmp_30 || !_tmp_28) && (_tmp_31 || !_tmp_29);
  reg [_tmp_32-1:0] __tmp_33_1;
  wire [32-1:0] _tmp_34;
  reg [32-1:0] __tmp_34_1;
  assign _tmp_34 = (__tmp_33_1)? ram_b_0_rdata : __tmp_34_1;
  reg [8-1:0] _tmp_35;
  reg _tmp_36;
  reg _tmp_37;
  reg _tmp_38;
  reg _tmp_39;
  reg [8-1:0] _tmp_40;
  reg _tmp_41;
  wire [32-1:0] _tmp_data_42;
  wire _tmp_valid_42;
  wire _tmp_ready_42;
  assign _tmp_ready_42 = (_tmp_40 > 0) && !_tmp_41;
  reg _ram_c_cond_0_1;
  reg [32-1:0] _tmp_fsm_2;
  localparam _tmp_fsm_2_init = 0;
  reg [9-1:0] _tmp_43;
  reg _master_cond_2_1;
  reg _tmp_44;
  reg _tmp_45;
  wire _tmp_46;
  wire _tmp_47;
  assign _tmp_47 = 1;
  localparam _tmp_48 = 1;
  wire [_tmp_48-1:0] _tmp_49;
  assign _tmp_49 = (_tmp_46 || !_tmp_44) && (_tmp_47 || !_tmp_45);
  reg [_tmp_48-1:0] __tmp_49_1;
  wire [32-1:0] _tmp_50;
  reg [32-1:0] __tmp_50_1;
  assign _tmp_50 = (__tmp_49_1)? ram_c_0_rdata : __tmp_50_1;
  reg [8-1:0] _tmp_51;
  reg _tmp_52;
  reg _tmp_53;
  reg _tmp_54;
  reg _tmp_55;
  reg _tmp_56;
  wire [32-1:0] _tmp_data_57;
  wire _tmp_valid_57;
  wire _tmp_ready_57;
  assign _tmp_ready_57 = (_tmp_fsm_2 == 3) && ((_tmp_43 > 0) && (master_wready || !master_wvalid));
  reg _master_cond_3_1;
  reg [32-1:0] sum;
  reg _seq_cond_0_1;
  reg [9-1:0] _tmp_58;
  reg [32-1:0] _tmp_59;
  reg _tmp_60;
  reg _tmp_61;
  assign slave_arready = (fsm == 8) && !_tmp_60 && _tmp_61;
  reg _tmp_62;
  reg _slave_cond_0_1;

  always @(posedge CLK) begin
    if(RST) begin
      _tmp_3 <= 0;
      _tmp_1 <= 0;
      _tmp_0 <= 0;
      _tmp_2 <= 0;
      _tmp_61 <= 0;
      _tmp_59 <= 0;
      _tmp_58 <= 0;
      _tmp_60 <= 0;
      slave_rdata <= 0;
      slave_rvalid <= 0;
      slave_rlast <= 0;
      _tmp_62 <= 0;
      _slave_cond_0_1 <= 0;
    end else begin
      if(_slave_cond_0_1) begin
        slave_rvalid <= 0;
        slave_rlast <= 0;
        _tmp_62 <= 0;
      end 
      _tmp_3 <= slave_awvalid;
      if(slave_awready && slave_awvalid) begin
        _tmp_1 <= slave_awaddr;
        _tmp_0 <= slave_awlen + 1;
      end 
      _tmp_2 <= slave_awready && slave_awvalid;
      if(slave_wready && slave_wvalid && (_tmp_0 > 0)) begin
        _tmp_0 <= _tmp_0 - 1;
      end 
      _tmp_61 <= slave_arvalid;
      if(slave_arready && slave_arvalid) begin
        _tmp_59 <= slave_araddr;
        _tmp_58 <= slave_arlen + 1;
      end 
      _tmp_60 <= slave_arready && slave_arvalid;
      if((fsm == 9) && ((_tmp_58 > 0) && (slave_rready || !slave_rvalid) && (_tmp_58 > 0))) begin
        slave_rdata <= sum;
        slave_rvalid <= 1;
        slave_rlast <= 0;
        _tmp_58 <= _tmp_58 - 1;
      end 
      if((fsm == 9) && ((_tmp_58 > 0) && (slave_rready || !slave_rvalid) && (_tmp_58 > 0)) && (_tmp_58 == 1)) begin
        slave_rlast <= 1;
        _tmp_62 <= 1;
      end 
      _slave_cond_0_1 <= 1;
      if(slave_rvalid && !slave_rready) begin
        slave_rvalid <= slave_rvalid;
        slave_rlast <= slave_rlast;
        _tmp_62 <= _tmp_62;
      end 
    end
  end


  always @(posedge CLK) begin
    if(RST) begin
      master_araddr <= 0;
      master_arlen <= 0;
      master_arvalid <= 0;
      _tmp_4 <= 0;
      _master_cond_0_1 <= 0;
      _tmp_10 <= 0;
      _master_cond_1_1 <= 0;
      master_awaddr <= 0;
      master_awlen <= 0;
      master_awvalid <= 0;
      _tmp_43 <= 0;
      _master_cond_2_1 <= 0;
      master_wdata <= 0;
      master_wvalid <= 0;
      master_wlast <= 0;
      master_wstrb <= 0;
      _tmp_56 <= 0;
      _master_cond_3_1 <= 0;
    end else begin
      if(_master_cond_0_1) begin
        master_arvalid <= 0;
      end 
      if(_master_cond_1_1) begin
        master_arvalid <= 0;
      end 
      if(_master_cond_2_1) begin
        master_awvalid <= 0;
      end 
      if(_master_cond_3_1) begin
        master_wvalid <= 0;
        master_wlast <= 0;
        _tmp_56 <= 0;
      end 
      if((_tmp_fsm_0 == 1) && ((master_arready || !master_arvalid) && (_tmp_4 == 0))) begin
        master_araddr <= 1024;
        master_arlen <= 63;
        master_arvalid <= 1;
        _tmp_4 <= 64;
      end 
      _master_cond_0_1 <= 1;
      if(master_arvalid && !master_arready) begin
        master_arvalid <= master_arvalid;
      end 
      if(master_rready && master_rvalid && (_tmp_4 > 0)) begin
        _tmp_4 <= _tmp_4 - 1;
      end 
      if((_tmp_fsm_1 == 1) && ((master_arready || !master_arvalid) && (_tmp_10 == 0))) begin
        master_araddr <= 2048;
        master_arlen <= 63;
        master_arvalid <= 1;
        _tmp_10 <= 64;
      end 
      _master_cond_1_1 <= 1;
      if(master_arvalid && !master_arready) begin
        master_arvalid <= master_arvalid;
      end 
      if(master_rready && master_rvalid && (_tmp_10 > 0)) begin
        _tmp_10 <= _tmp_10 - 1;
      end 
      if((_tmp_fsm_2 == 1) && ((master_awready || !master_awvalid) && (_tmp_43 == 0))) begin
        master_awaddr <= 3072;
        master_awlen <= 63;
        master_awvalid <= 1;
        _tmp_43 <= 64;
      end 
      if((_tmp_fsm_2 == 1) && ((master_awready || !master_awvalid) && (_tmp_43 == 0)) && 0) begin
        master_awvalid <= 0;
      end 
      _master_cond_2_1 <= 1;
      if(master_awvalid && !master_awready) begin
        master_awvalid <= master_awvalid;
      end 
      if(_tmp_valid_57 && ((_tmp_fsm_2 == 3) && ((_tmp_43 > 0) && (master_wready || !master_wvalid))) && ((_tmp_43 > 0) && (master_wready || !master_wvalid) && (_tmp_43 > 0))) begin
        master_wdata <= _tmp_data_57;
        master_wvalid <= 1;
        master_wlast <= 0;
        master_wstrb <= { 4{ 1'd1 } };
        _tmp_43 <= _tmp_43 - 1;
      end 
      if(_tmp_valid_57 && ((_tmp_fsm_2 == 3) && ((_tmp_43 > 0) && (master_wready || !master_wvalid))) && ((_tmp_43 > 0) && (master_wready || !master_wvalid) && (_tmp_43 > 0)) && (_tmp_43 == 1)) begin
        master_wlast <= 1;
        _tmp_56 <= 1;
      end 
      _master_cond_3_1 <= 1;
      if(master_wvalid && !master_wready) begin
        master_wvalid <= master_wvalid;
        master_wlast <= master_wlast;
        _tmp_56 <= _tmp_56;
      end 
    end
  end

  assign _tmp_data_9 = master_rdata;
  assign _tmp_valid_9 = master_rvalid;
  assign _tmp_5 = 1 && _tmp_ready_9;
  assign _tmp_data_15 = master_rdata;
  assign _tmp_valid_15 = master_rvalid;
  assign _tmp_11 = 1 && _tmp_ready_15;

  always @(posedge CLK) begin
    if(RST) begin
      ram_a_0_addr <= 0;
      _tmp_7 <= 0;
      ram_a_0_wdata <= 0;
      ram_a_0_wenable <= 0;
      _tmp_8 <= 0;
      _ram_a_cond_0_1 <= 0;
      __tmp_21_1 <= 0;
      __tmp_22_1 <= 0;
      _tmp_27 <= 0;
      _tmp_16 <= 0;
      _tmp_17 <= 0;
      _tmp_25 <= 0;
      _tmp_26 <= 0;
      _tmp_24 <= 0;
      _tmp_23 <= 0;
    end else begin
      if(_ram_a_cond_0_1) begin
        ram_a_0_wenable <= 0;
        _tmp_8 <= 0;
      end 
      if((_tmp_fsm_0 == 2) && (_tmp_7 == 0)) begin
        ram_a_0_addr <= -1;
        _tmp_7 <= 64;
      end 
      if(_tmp_valid_9 && ((_tmp_7 > 0) && !_tmp_8) && (_tmp_7 > 0)) begin
        ram_a_0_addr <= ram_a_0_addr + 1;
        ram_a_0_wdata <= _tmp_data_9;
        ram_a_0_wenable <= 1;
        _tmp_7 <= _tmp_7 - 1;
      end 
      if(_tmp_valid_9 && ((_tmp_7 > 0) && !_tmp_8) && (_tmp_7 == 1)) begin
        _tmp_8 <= 1;
      end 
      _ram_a_cond_0_1 <= 1;
      __tmp_21_1 <= _tmp_21;
      __tmp_22_1 <= _tmp_22;
      if((_tmp_18 || !_tmp_16) && (_tmp_19 || !_tmp_17) && _tmp_25) begin
        _tmp_27 <= 0;
        _tmp_16 <= 0;
        _tmp_17 <= 0;
        _tmp_25 <= 0;
      end 
      if((_tmp_18 || !_tmp_16) && (_tmp_19 || !_tmp_17) && _tmp_24) begin
        _tmp_16 <= 1;
        _tmp_17 <= 1;
        _tmp_27 <= _tmp_26;
        _tmp_26 <= 0;
        _tmp_24 <= 0;
        _tmp_25 <= 1;
      end 
      if((fsm == 4) && (_tmp_23 == 0) && !_tmp_26 && !_tmp_27) begin
        ram_a_0_addr <= 0;
        _tmp_23 <= 63;
        _tmp_24 <= 1;
      end 
      if((_tmp_18 || !_tmp_16) && (_tmp_19 || !_tmp_17) && (_tmp_23 > 0)) begin
        ram_a_0_addr <= ram_a_0_addr + 1;
        _tmp_23 <= _tmp_23 - 1;
        _tmp_24 <= 1;
        _tmp_26 <= 0;
      end 
      if((_tmp_18 || !_tmp_16) && (_tmp_19 || !_tmp_17) && (_tmp_23 == 1)) begin
        _tmp_26 <= 1;
      end 
    end
  end

  reg [32-1:0] _tmp_data_63;
  reg _tmp_valid_63;
  wire _tmp_ready_63;
  assign _tmp_18 = 1 && ((_tmp_ready_63 || !_tmp_valid_63) && (_tmp_16 && _tmp_28));
  assign _tmp_30 = 1 && ((_tmp_ready_63 || !_tmp_valid_63) && (_tmp_16 && _tmp_28));
  assign _tmp_data_42 = _tmp_data_63;
  assign _tmp_valid_42 = _tmp_valid_63;
  assign _tmp_ready_63 = _tmp_ready_42;

  always @(posedge CLK) begin
    if(RST) begin
      _tmp_data_63 <= 0;
      _tmp_valid_63 <= 0;
    end else begin
      if((_tmp_ready_63 || !_tmp_valid_63) && (_tmp_18 && _tmp_30) && (_tmp_16 && _tmp_28)) begin
        _tmp_data_63 <= _tmp_22 + _tmp_34;
      end 
      if(_tmp_valid_63 && _tmp_ready_63) begin
        _tmp_valid_63 <= 0;
      end 
      if((_tmp_ready_63 || !_tmp_valid_63) && (_tmp_18 && _tmp_30)) begin
        _tmp_valid_63 <= _tmp_16 && _tmp_28;
      end 
    end
  end


  always @(posedge CLK) begin
    if(RST) begin
      ram_b_0_addr <= 0;
      _tmp_13 <= 0;
      ram_b_0_wdata <= 0;
      ram_b_0_wenable <= 0;
      _tmp_14 <= 0;
      _ram_b_cond_0_1 <= 0;
      __tmp_33_1 <= 0;
      __tmp_34_1 <= 0;
      _tmp_39 <= 0;
      _tmp_28 <= 0;
      _tmp_29 <= 0;
      _tmp_37 <= 0;
      _tmp_38 <= 0;
      _tmp_36 <= 0;
      _tmp_35 <= 0;
    end else begin
      if(_ram_b_cond_0_1) begin
        ram_b_0_wenable <= 0;
        _tmp_14 <= 0;
      end 
      if((_tmp_fsm_1 == 2) && (_tmp_13 == 0)) begin
        ram_b_0_addr <= -1;
        _tmp_13 <= 64;
      end 
      if(_tmp_valid_15 && ((_tmp_13 > 0) && !_tmp_14) && (_tmp_13 > 0)) begin
        ram_b_0_addr <= ram_b_0_addr + 1;
        ram_b_0_wdata <= _tmp_data_15;
        ram_b_0_wenable <= 1;
        _tmp_13 <= _tmp_13 - 1;
      end 
      if(_tmp_valid_15 && ((_tmp_13 > 0) && !_tmp_14) && (_tmp_13 == 1)) begin
        _tmp_14 <= 1;
      end 
      _ram_b_cond_0_1 <= 1;
      __tmp_33_1 <= _tmp_33;
      __tmp_34_1 <= _tmp_34;
      if((_tmp_30 || !_tmp_28) && (_tmp_31 || !_tmp_29) && _tmp_37) begin
        _tmp_39 <= 0;
        _tmp_28 <= 0;
        _tmp_29 <= 0;
        _tmp_37 <= 0;
      end 
      if((_tmp_30 || !_tmp_28) && (_tmp_31 || !_tmp_29) && _tmp_36) begin
        _tmp_28 <= 1;
        _tmp_29 <= 1;
        _tmp_39 <= _tmp_38;
        _tmp_38 <= 0;
        _tmp_36 <= 0;
        _tmp_37 <= 1;
      end 
      if((fsm == 4) && (_tmp_35 == 0) && !_tmp_38 && !_tmp_39) begin
        ram_b_0_addr <= 0;
        _tmp_35 <= 63;
        _tmp_36 <= 1;
      end 
      if((_tmp_30 || !_tmp_28) && (_tmp_31 || !_tmp_29) && (_tmp_35 > 0)) begin
        ram_b_0_addr <= ram_b_0_addr + 1;
        _tmp_35 <= _tmp_35 - 1;
        _tmp_36 <= 1;
        _tmp_38 <= 0;
      end 
      if((_tmp_30 || !_tmp_28) && (_tmp_31 || !_tmp_29) && (_tmp_35 == 1)) begin
        _tmp_38 <= 1;
      end 
    end
  end


  always @(posedge CLK) begin
    if(RST) begin
      ram_c_0_addr <= 0;
      _tmp_40 <= 0;
      ram_c_0_wdata <= 0;
      ram_c_0_wenable <= 0;
      _tmp_41 <= 0;
      _ram_c_cond_0_1 <= 0;
      __tmp_49_1 <= 0;
      __tmp_50_1 <= 0;
      _tmp_55 <= 0;
      _tmp_44 <= 0;
      _tmp_45 <= 0;
      _tmp_53 <= 0;
      _tmp_54 <= 0;
      _tmp_52 <= 0;
      _tmp_51 <= 0;
    end else begin
      if(_ram_c_cond_0_1) begin
        ram_c_0_wenable <= 0;
        _tmp_41 <= 0;
      end 
      if((fsm == 4) && (_tmp_40 == 0)) begin
        ram_c_0_addr <= -1;
        _tmp_40 <= 64;
      end 
      if(_tmp_valid_42 && ((_tmp_40 > 0) && !_tmp_41) && (_tmp_40 > 0)) begin
        ram_c_0_addr <= ram_c_0_addr + 1;
        ram_c_0_wdata <= _tmp_data_42;
        ram_c_0_wenable <= 1;
        _tmp_40 <= _tmp_40 - 1;
      end 
      if(_tmp_valid_42 && ((_tmp_40 > 0) && !_tmp_41) && (_tmp_40 == 1)) begin
        _tmp_41 <= 1;
      end 
      _ram_c_cond_0_1 <= 1;
      __tmp_49_1 <= _tmp_49;
      __tmp_50_1 <= _tmp_50;
      if((_tmp_46 || !_tmp_44) && (_tmp_47 || !_tmp_45) && _tmp_53) begin
        _tmp_55 <= 0;
        _tmp_44 <= 0;
        _tmp_45 <= 0;
        _tmp_53 <= 0;
      end 
      if((_tmp_46 || !_tmp_44) && (_tmp_47 || !_tmp_45) && _tmp_52) begin
        _tmp_44 <= 1;
        _tmp_45 <= 1;
        _tmp_55 <= _tmp_54;
        _tmp_54 <= 0;
        _tmp_52 <= 0;
        _tmp_53 <= 1;
      end 
      if((_tmp_fsm_2 == 2) && (_tmp_51 == 0) && !_tmp_54 && !_tmp_55) begin
        ram_c_0_addr <= 0;
        _tmp_51 <= 63;
        _tmp_52 <= 1;
      end 
      if((_tmp_46 || !_tmp_44) && (_tmp_47 || !_tmp_45) && (_tmp_51 > 0)) begin
        ram_c_0_addr <= ram_c_0_addr + 1;
        _tmp_51 <= _tmp_51 - 1;
        _tmp_52 <= 1;
        _tmp_54 <= 0;
      end 
      if((_tmp_46 || !_tmp_44) && (_tmp_47 || !_tmp_45) && (_tmp_51 == 1)) begin
        _tmp_54 <= 1;
      end 
    end
  end

  assign _tmp_data_57 = _tmp_50;
  assign _tmp_valid_57 = _tmp_44;
  assign _tmp_46 = 1 && _tmp_ready_57;
  localparam fsm_1 = 1;
  localparam fsm_2 = 2;
  localparam fsm_3 = 3;
  localparam fsm_4 = 4;
  localparam fsm_5 = 5;
  localparam fsm_6 = 6;
  localparam fsm_7 = 7;
  localparam fsm_8 = 8;
  localparam fsm_9 = 9;
  localparam fsm_10 = 10;

  always @(posedge CLK) begin
    if(RST) begin
      fsm <= fsm_init;
    end else begin
      case(fsm)
        fsm_init: begin
          if(_tmp_2) begin
            fsm <= fsm_1;
          end 
        end
        fsm_1: begin
          if(slave_wready && slave_wvalid) begin
            fsm <= fsm_2;
          end 
        end
        fsm_2: begin
          if(_tmp_8) begin
            fsm <= fsm_3;
          end 
        end
        fsm_3: begin
          if(_tmp_14) begin
            fsm <= fsm_4;
          end 
        end
        fsm_4: begin
          fsm <= fsm_5;
        end
        fsm_5: begin
          if(_tmp_41) begin
            fsm <= fsm_6;
          end 
        end
        fsm_6: begin
          if(_tmp_56) begin
            fsm <= fsm_7;
          end 
        end
        fsm_7: begin
          if(master_wvalid && master_wready && master_wlast) begin
            fsm <= fsm_8;
          end 
        end
        fsm_8: begin
          if(_tmp_60) begin
            fsm <= fsm_9;
          end 
        end
        fsm_9: begin
          if(_tmp_62) begin
            fsm <= fsm_10;
          end 
        end
        fsm_10: begin
          fsm <= fsm_init;
        end
      endcase
    end
  end

  localparam _tmp_fsm_0_1 = 1;
  localparam _tmp_fsm_0_2 = 2;
  localparam _tmp_fsm_0_3 = 3;

  always @(posedge CLK) begin
    if(RST) begin
      _tmp_fsm_0 <= _tmp_fsm_0_init;
    end else begin
      case(_tmp_fsm_0)
        _tmp_fsm_0_init: begin
          if(fsm == 2) begin
            _tmp_fsm_0 <= _tmp_fsm_0_1;
          end 
        end
        _tmp_fsm_0_1: begin
          if(master_arready || !master_arvalid) begin
            _tmp_fsm_0 <= _tmp_fsm_0_2;
          end 
        end
        _tmp_fsm_0_2: begin
          _tmp_fsm_0 <= _tmp_fsm_0_3;
        end
        _tmp_fsm_0_3: begin
          if(_tmp_8) begin
            _tmp_fsm_0 <= _tmp_fsm_0_init;
          end 
        end
      endcase
    end
  end

  localparam _tmp_fsm_1_1 = 1;
  localparam _tmp_fsm_1_2 = 2;
  localparam _tmp_fsm_1_3 = 3;

  always @(posedge CLK) begin
    if(RST) begin
      _tmp_fsm_1 <= _tmp_fsm_1_init;
    end else begin
      case(_tmp_fsm_1)
        _tmp_fsm_1_init: begin
          if(fsm == 3) begin
            _tmp_fsm_1 <= _tmp_fsm_1_1;
          end 
        end
        _tmp_fsm_1_1: begin
          if(master_arready || !master_arvalid) begin
            _tmp_fsm_1 <= _tmp_fsm_1_2;
          end 
        end
        _tmp_fsm_1_2: begin
          _tmp_fsm_1 <= _tmp_fsm_1_3;
        end
        _tmp_fsm_1_3: begin
          if(_tmp_14) begin
            _tmp_fsm_1 <= _tmp_fsm_1_init;
          end 
        end
      endcase
    end
  end

  localparam _tmp_fsm_2_1 = 1;
  localparam _tmp_fsm_2_2 = 2;
  localparam _tmp_fsm_2_3 = 3;

  always @(posedge CLK) begin
    if(RST) begin
      _tmp_fsm_2 <= _tmp_fsm_2_init;
    end else begin
      case(_tmp_fsm_2)
        _tmp_fsm_2_init: begin
          if(fsm == 6) begin
            _tmp_fsm_2 <= _tmp_fsm_2_1;
          end 
        end
        _tmp_fsm_2_1: begin
          if(master_awready || !master_awvalid) begin
            _tmp_fsm_2 <= _tmp_fsm_2_2;
          end 
        end
        _tmp_fsm_2_2: begin
          _tmp_fsm_2 <= _tmp_fsm_2_3;
        end
        _tmp_fsm_2_3: begin
          if(_tmp_56) begin
            _tmp_fsm_2 <= _tmp_fsm_2_init;
          end 
        end
      endcase
    end
  end


  always @(posedge CLK) begin
    if(RST) begin
      sum <= 0;
      _seq_cond_0_1 <= 0;
    end else begin
      if(_seq_cond_0_1) begin
        $display("sum=%d expected_sum=%d", sum, 200640);
      end 
      if(fsm == 0) begin
        sum <= 0;
      end 
      if(master_wvalid && master_wready) begin
        sum <= sum + master_wdata;
      end 
      _seq_cond_0_1 <= master_wvalid && master_wready && master_wlast;
    end
  end


endmodule



module ram_a
(
  input CLK,
  input [10-1:0] ram_a_0_addr,
  output [32-1:0] ram_a_0_rdata,
  input [32-1:0] ram_a_0_wdata,
  input ram_a_0_wenable
);

  reg [10-1:0] ram_a_0_daddr;
  reg [32-1:0] mem [0:1024-1];

  always @(posedge CLK) begin
    if(ram_a_0_wenable) begin
      mem[ram_a_0_addr] <= ram_a_0_wdata;
    end 
    ram_a_0_daddr <= ram_a_0_addr;
  end

  assign ram_a_0_rdata = mem[ram_a_0_daddr];

endmodule



module ram_b
(
  input CLK,
  input [10-1:0] ram_b_0_addr,
  output [32-1:0] ram_b_0_rdata,
  input [32-1:0] ram_b_0_wdata,
  input ram_b_0_wenable
);

  reg [10-1:0] ram_b_0_daddr;
  reg [32-1:0] mem [0:1024-1];

  always @(posedge CLK) begin
    if(ram_b_0_wenable) begin
      mem[ram_b_0_addr] <= ram_b_0_wdata;
    end 
    ram_b_0_daddr <= ram_b_0_addr;
  end

  assign ram_b_0_rdata = mem[ram_b_0_daddr];

endmodule



module ram_c
(
  input CLK,
  input [10-1:0] ram_c_0_addr,
  output [32-1:0] ram_c_0_rdata,
  input [32-1:0] ram_c_0_wdata,
  input ram_c_0_wenable
);

  reg [10-1:0] ram_c_0_daddr;
  reg [32-1:0] mem [0:1024-1];

  always @(posedge CLK) begin
    if(ram_c_0_wenable) begin
      mem[ram_c_0_addr] <= ram_c_0_wdata;
    end 
    ram_c_0_daddr <= ram_c_0_addr;
  end

  assign ram_c_0_rdata = mem[ram_c_0_daddr];

endmodule
"""


def test():
    veriloggen.reset()
    test_module = axi_vecadd.mkTest()
    code = test_module.to_verilog()

    from pyverilog.vparser.parser import VerilogParser
    from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
    parser = VerilogParser()
    expected_ast = parser.parse(expected_verilog)
    codegen = ASTCodeGenerator()
    expected_code = codegen.visit(expected_ast)

    assert(expected_code == code)
