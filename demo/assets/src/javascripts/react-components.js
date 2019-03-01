import { ReactDOM } from 'react-dom'
import Header from '../../../../hmlr_design_system/components/header/component'
window.Header = Header

window.application_config = JSON.parse(document.getElementById('application_config').innerHTML)
