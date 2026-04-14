import React, { useEffect } from 'react';
import { Navbar } from '../components/Navbar';
import { useWallet } from '../context/WalletContext';
import { useNavigate, Link } from 'react-router-dom';
import { Search, Award, Activity, History, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';
import SpotlightCard from '../components/SpotlightCard';

export const Dashboard = () => {
  const { walletAddress } = useWallet();
  const navigate = useNavigate();

  useEffect(() => {
    if (!walletAddress) {
      navigate('/');
    }
  }, [walletAddress, navigate]);

  if (!walletAddress) return null;

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Navbar />

      <main className="flex-grow max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 w-full">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <h1 className="text-4xl font-syne font-bold mb-2">Welcome Back, <span className="text-secondary font-mono text-3xl">{walletAddress.slice(0, 8)}...</span></h1>
          <p className="text-gray-400">Manage your smart contracts securely via AlgoShield AI.</p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {/* Scan Action */}
          <Link to="/scan" className="group">
            <motion.div className="h-full" whileHover={{ y: -5 }}>
              <SpotlightCard className="h-full flex flex-col justify-between" spotlightColor="rgba(0, 255, 136, 0.2)">
                <div>
                  <Search className="w-10 h-10 text-primary mb-4 group-hover:text-white transition-colors" />
                  <h3 className="text-xl font-syne font-bold mb-2 text-white">Scan a Contract</h3>
                  <p className="text-gray-400 text-sm">Upload Teal code or provide App ID for comprehensive security audit.</p>
                </div>
                <div className="mt-6 flex justify-end">
                  <ArrowRight className="w-5 h-5 text-primary group-hover:translate-x-2 transition-transform" />
                </div>
              </SpotlightCard>
            </motion.div>
          </Link>

          {/* Certificates Action */}
          <Link to="/certificates" className="group">
            <motion.div className="h-full" whileHover={{ y: -5 }}>
              <SpotlightCard className="h-full flex flex-col justify-between border-t border-warning/50" spotlightColor="rgba(255, 170, 0, 0.2)">
                <div>
                  <Award className="w-10 h-10 text-warning mb-4 group-hover:text-white transition-colors" />
                  <h3 className="text-xl font-syne font-bold mb-2 text-white">My Certificates</h3>
                  <p className="text-gray-400 text-sm">View and manage your minted on-chain security certificates.</p>
                </div>
                <div className="mt-6 flex justify-end">
                  <ArrowRight className="w-5 h-5 text-warning group-hover:translate-x-2 transition-transform" />
                </div>
              </SpotlightCard>
            </motion.div>
          </Link>

          {/* Monitor Action */}
          <Link to="/monitor" className="group">
            <motion.div className="h-full" whileHover={{ y: -5 }}>
              <SpotlightCard className="h-full flex flex-col justify-between border-t border-secondary/50" spotlightColor="rgba(0, 212, 255, 0.2)">
                <div>
                  <Activity className="w-10 h-10 text-secondary mb-4 group-hover:text-white transition-colors" />
                  <h3 className="text-xl font-syne font-bold mb-2 text-white">Monitor Contract</h3>
                  <p className="text-gray-400 text-sm">Set up 24/7 AI-powered anomaly detection for live smart contracts.</p>
                </div>
                <div className="mt-6 flex justify-end">
                  <ArrowRight className="w-5 h-5 text-secondary group-hover:translate-x-2 transition-transform" />
                </div>
              </SpotlightCard>
            </motion.div>
          </Link>
        </div>

        {/* Activity Feed */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
        >
          <SpotlightCard spotlightColor="rgba(255, 255, 255, 0.1)">
            <div className="flex items-center gap-3 mb-6 border-b border-border pb-4">
              <History className="w-6 h-6 text-gray-400" />
              <h2 className="text-2xl font-syne font-bold">Recent Scans</h2>
            </div>
            
            <div className="space-y-4">
              {/* Dummy Data for Recent Scans */}
            <div className="flex justify-between items-center p-4 bg-surface-hover rounded-lg border border-border">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full border-2 border-primary flex justify-center items-center font-mono font-bold text-primary text-sm shadow-[0_0_10px_rgba(0,255,136,0.3)]">
                  92
                </div>
                <div>
                  <h4 className="font-syne font-bold text-lg">App ID: 1234567</h4>
                  <p className="text-xs text-gray-400 font-mono">2 mins ago</p>
                </div>
              </div>
              <div>
                <span className="px-3 py-1 bg-safe/20 text-safe border border-safe/50 rounded-full font-mono text-xs">SAFE</span>
              </div>
            </div>

            <div className="flex justify-between items-center p-4 bg-surface-hover rounded-lg border border-border">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full border-2 border-danger flex justify-center items-center font-mono font-bold text-danger text-sm shadow-[0_0_10px_rgba(255,51,51,0.3)]">
                  34
                </div>
                <div>
                  <h4 className="font-syne font-bold text-lg">Untitled.teal</h4>
                  <p className="text-xs text-gray-400 font-mono">1 hour ago</p>
                </div>
              </div>
              <div>
                <span className="px-3 py-1 bg-danger/20 text-danger border border-danger/50 rounded-full font-mono text-xs">CRITICAL</span>
              </div>
            </div>
            
            <div className="flex justify-between items-center p-4 bg-surface-hover rounded-lg border border-border">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full border-2 border-warning flex justify-center items-center font-mono font-bold text-warning text-sm shadow-[0_0_10px_rgba(255,170,0,0.3)]">
                  65
                </div>
                <div>
                  <h4 className="font-syne font-bold text-lg">App ID: 987654</h4>
                  <p className="text-xs text-gray-400 font-mono">Yesterday</p>
                </div>
              </div>
              <div>
                <span className="px-3 py-1 bg-warning/20 text-warning border border-warning/50 rounded-full font-mono text-xs">RISKY</span>
              </div>
              </div>
            </div>
          </SpotlightCard>
        </motion.div>
      </main>
    </div>
  );
};
