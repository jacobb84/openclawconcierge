import { useState } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  Music, 
  Calendar, 
  Newspaper, 
  Briefcase, 
  LogOut,
  LayoutDashboard,
  Menu,
  X
} from 'lucide-react';

const navItems = [
  { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/concerts', icon: Music, label: 'Concerts' },
  { to: '/events', icon: Calendar, label: 'Events' },
  { to: '/news', icon: Newspaper, label: 'News' },
  { to: '/career', icon: Briefcase, label: 'Career' },
];

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const closeSidebar = () => setSidebarOpen(false);

  return (
    <div className="layout">
      {/* Mobile header with hamburger */}
      <header className="mobile-header">
        <button className="hamburger-btn" onClick={() => setSidebarOpen(true)}>
          <Menu className="w-6 h-6" />
        </button>
        <div className="mobile-brand">
          <span className="sidebar-title">OpenClaw</span>
          <span className="sidebar-subtitle">Concierge</span>
        </div>
      </header>

      {/* Overlay for mobile */}
      {sidebarOpen && <div className="sidebar-overlay" onClick={closeSidebar} />}

      <aside className={`sidebar ${sidebarOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-header">
          <div className="sidebar-header-content">
            <h1 className="sidebar-title">OpenClaw</h1>
            <p className="sidebar-subtitle">Concierge</p>
          </div>
          <button className="sidebar-close-btn" onClick={closeSidebar}>
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <nav className="sidebar-nav">
          <ul>
            {navItems.map((item) => (
              <li key={item.to}>
                <NavLink
                  to={item.to}
                  end={item.to === '/'}
                  className={({ isActive }) =>
                    `nav-link ${isActive ? 'active' : ''}`
                  }
                  onClick={closeSidebar}
                >
                  <item.icon className="w-5 h-5" />
                  {item.label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>

        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-avatar">
              {user?.username?.charAt(0).toUpperCase()}
            </div>
            <span className="user-name">{user?.username}</span>
          </div>
          <button onClick={handleLogout} className="logout-btn">
            <LogOut className="w-5 h-5" />
            Sign out
          </button>
        </div>
      </aside>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
