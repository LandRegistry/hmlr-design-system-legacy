import React from 'react'

function Footer (props) {
  const links = props.children && <>
    <h2 className='govuk-visually-hidden'>Support links</h2>
    <ul className='hmlr-footer__links'>
      { React.Children.map(props.children, (item, index) => (
        <li className='hmlr-footer__item' key={index}>
          {React.cloneElement(item, { className: 'hmlr-footer__link' })}
        </li>
      ))}
    </ul>
  </>

  return <footer className='hmlr-footer'>
    <div className='hmlr-footer__inner'>
      { links}
    </div>
  </footer>
}

export default Footer
